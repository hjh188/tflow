#!/usr/bin/env python

import re
import importlib

from operator import itemgetter

import django.db.models
from django.db import connection

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.fields import SerializerMethodField

from django_logging import log, ErrorLogObject

from lucommon.decorator import format_response
from lucommon import (
    pagination,
    exception,
)

from lucommon import filters as lufilters
from lucommon.response import LuResponse
from lucommon.logger import lu_logger

#from lucommon import settings
# Use from django.conf, so that user could
# reset setting value in project setting without
# do modification on lucommon settings
from django.conf import settings
from lucommon import status
from lucommon import auth

from lucommon.utils import (
   ReturnList,
)

from lucommon.sql import LuSQL

from lucommon.confs import DummyLuConf

from reversion import revisions

"""
Lu common viewsets
"""


class LuModelViewSet(viewsets.ModelViewSet,
                     exception.LuExceptionHandler,
                     lufilters.LuDefaultCustomFilter):
    """
    In order to do something(like log, customed response data, etc) that
    happens inside REST framework we need to override the .dispatch() method
    that is called as soon as the view is entered.
    """
    # Default Paging class
    pagination_class = pagination.LuPagination

    # Filter backends
    lufilters.LuSearchFilter.search_param = settings.SEARCH_PARAM
    filter_backends = (filters.DjangoFilterBackend, lufilters.LuSearchFilter,) if settings.SEARCH_ENABLE \
                      else (filters.DjangoFilterBackend,)

    # Ordering filter
    lufilters.LuOrderingFilter.ordering_param = settings.ORDERING_PARAM
    filter_backends += (lufilters.LuOrderingFilter,) if settings.ORDERING_ENABLE else ()
    ordering_fields = '__all__'

    # Set code base default filter
    filter_queryset = lufilters.LuDefaultCustomFilter.filter_queryset

    # Set exception handler
    handle_exception = exception.LuExceptionHandler.handle_exception

    # Set auth related
    authentication_classes = auth.LuAuthPerm.authentication_classes
    permission_classes = auth.LuAuthPerm.permission_classes

    def initialize_request(self, request, *args, **kwargs):
        """
        Override initial_request for more detail control
        """
        request = super(LuModelViewSet, self).initialize_request(request, *args, **kwargs)

        # Do something here
        if settings.RESPONSE_MODE in request.query_params:
            if request.query_params.get(settings.RESPONSE_MODE) == settings.RESPONSE_DEBUG_MODE:
                self.pagination_class = pagination.LuPagination2

        # Process for the pagination
        if request.query_params.get(settings.LIMIT_FIELD) == settings.UNLIMIT:
            self.pagination_class = None

        # As history issue, lucommon didn't set conf for the viewset,
        # So do it here if not for the version compatible
        # In the future, we actually can remove below code block
        if not hasattr(self, 'conf'):
            patten = re.compile(r"'(.*)'")
            conf_list = patten.search(str(self.__class__)).groups()[0].\
                        replace('views', 'confs').replace('ViewSet', 'Conf').split('.')
            conf_module = '.'.join(conf_list[0:2])
            conf_name = conf_list[2]
            try:
                setattr(self, 'conf', getattr(importlib.import_module(conf_module), conf_name))
            except Exception, err:
                setattr(self, 'conf', DummyLuConf)

            # Set default attribute
            if not hasattr(self.conf, 'sql_injection_allow'):
                setattr(self.conf, 'sql_injection_allow', ['SELECT'])

            if not hasattr(self.conf, 'sql_injection_map'):
                setattr(self.conf, 'sql_injection_map', {})

            if not hasattr(self.conf, 'enable_join_multiple_key_value_pair'):
                setattr(self.conf, 'enable_join_multiple_key_value_pair', True)

            if not hasattr(self.conf, 'join_multiple_key_value_pair_delimiter'):
                setattr(self.conf, 'join_multiple_key_value_pair_delimiter', ',')

            if not hasattr(self.conf, 'enable_reversion_post'):
                setattr(self.conf, 'enable_reversion_post', False)

            if not hasattr(self.conf, 'enable_reversion_update'):
                setattr(self.conf, 'enable_reversion_update', False)

            if not hasattr(self.conf, 'enable_reversion_partial_update'):
                setattr(self.conf, 'enable_reversion_partial_update', False)

            if not hasattr(self.conf, 'enable_reversion_delete'):
                setattr(self.conf, 'enable_reversion_delete', False)

        return request

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch
        """
        try:
            response = super(LuModelViewSet, self).dispatch(request, *args, **kwargs)
        except Exception, err:
            log.error(ErrorLogObject(request, err))
            response = LuResponse(code=status.LU_5000_SERVER_ERROR, message=str(err))

        return response



    def list(self, request, *args, **kwargs):
        """
        HTTP GET list entry
        """
        # Common process: response field, check if need to do in database level
        response_field = request.query_params.get(settings.RESPONSE_FIELD,'')
        queryset = self.queryset

        # If not method field in serializer class, we will use response_field in DATABASE level
        if not self.serializer_class._declared_fields and response_field:
            response_fields = response_field.split(settings.RESPONSE_FIELD_DELIMITER)
            queryset = queryset.values(*response_fields)

        # Common process: check if need to record distinct in database level
        _distinct = request.query_params.get(settings.RESPONSE_DISTINCT, '')
        if _distinct == self.response_distinct:
            queryset = queryset.distinct()

        self.queryset = queryset

        # Process for the aggregate function: Count, Max, Min, Avg
        #and won't process for `lu_response_field`
        # Works for SQL: SELECT item1, count(item1) FROM table1 WHERE (Condition) GROUP BY item1 ORDER BY count(item1)
        full_search_type_list = request.query_params.get(settings.SEARCH_TYPE, self.SEARCH_TYPE.contain).split(settings.SEARCH_TYPE_DELIMITER)
        if set(full_search_type_list) & set([self.SEARCH_TYPE.count, self.SEARCH_TYPE.max, self.SEARCH_TYPE.min, self.SEARCH_TYPE.avg]):
            # Put aggregate search type in the last, as we may group by multiple fields
            if full_search_type_list[-1] not in [self.SEARCH_TYPE.count, self.SEARCH_TYPE.max, self.SEARCH_TYPE.min, self.SEARCH_TYPE.avg]:
                return LuResponse(code = status.LU_4007_INVALID_PARAM,
                         message = 'Please put aggregate func type in the last of `lu_search_type`!')

            search_field = request.query_params.get(settings.SEARCH_KEY)

            if not search_field:
                return LuResponse(code = status.LU_4010_PARAM_NEEDED,
                         message = 'Please specify param `lu_search_field` for the search field!')

            group_field = request.query_params.get(settings.GROUP_PARAM)
            if not group_field:
                return LuResponse(code = status.LU_4010_PARAM_NEEDED,
                         message = 'Please specify param `lu_group_field` for the search field!')

            group_field_list = group_field.split(settings.GROUP_PARAM_DELIMITER)
            full_search_field_list = search_field.split(settings.SEARCH_KEY_DELIMITER)

            if len(full_search_type_list) > len(full_search_field_list):
                return LuResponse(code = status.LU_4007_INVALID_PARAM,
                         message = 'The number of `lu_search_field` should not less than the number of `lu_search_type`!')

            type_number = len(full_search_type_list)
            aggregate_search_field_list = full_search_field_list[type_number-1:]
            aggregate_search_type = full_search_type_list[-1]

            queryset = self.queryset
            # Process for LuSearchFilter for complex filter firstly
            if len(full_search_type_list) > 1:
                common_search_field_list = full_search_field_list[0:type_number-1]
                common_search_type_list = full_search_type_list[0:type_number-1]

                common_search_word_list = request.query_params.get(settings.SEARCH_PARAM, '').split(settings.SEARCH_PARAM_DELIMITER)

                if len(common_search_word_list) < type_number -1:
                    return LuResponse(code = status.LU_4007_INVALID_PARAM,
                             message = 'The number of `lu_search_word` should not less than %d' % (type_number -1))

                self.search_fields = ()
                self.search_words = ()
                for index, lu_key in enumerate(common_search_field_list):
                    try:
                        prefix = self.search_type_map[common_search_type_list[index]]
                    except:
                        prefix = ''

                    if common_search_type_list[index] == self.SEARCH_TYPE._in:
                        # SQL IN: better performance for the string re
                        kwargs = {'%s__in' % lu_key: common_search_word_list[index].split(settings.SEARCH_PARAM_IN_DELIMITER)}
                        queryset = queryset.filter(**kwargs)
                        continue

                    if common_search_type_list[index] == self.SEARCH_TYPE._not_in:
                        # SQL NOT IN: better performance for the string re
                        kwargs = {'%s__in' % lu_key: common_search_word_list[index].split(settings.SEARCH_PARAM_NOTIN_DELIMITER)}
                        queryset = queryset.exclude(**kwargs)
                        continue

                    key = prefix + lu_key
                    self.search_fields += (key,)
                    self.search_words += (common_search_word_list[index],)

                queryset = self.filter_search_by_request_query_params(request, queryset)

            # Process for basic exact item match filter
            queryset = self.filter_by_request_query_params(request, queryset)
            #queryset = self.filter_by_request_query_params_order(request, queryset)

            order_field = ''
            if request.query_params.get(settings.ORDERING_PARAM):
                order_field = request.query_params.get(settings.ORDERING_PARAM, '')

            #queryset = queryset.values(*aggregate_search_field_list)
            # Check if DateTimeField in `group_field_list`, if yes, default, we will convert it
            # to day, user could also use `lu_date_format` to set ('year', 'month', 'day', 'hour', 'minute', 'second')
            for index, group_item in enumerate(group_field_list):
                for field in self.serializer_class.Meta.model._meta.local_fields:
                    if group_item == field.name and isinstance(field, django.db.models.fields.DateTimeField):
                        date_type = request.query_params.get(settings.DATE_TYPE, 'day')
                        truncate_date = connection.ops.date_trunc_sql(date_type, group_item)
                        convert_item_name = '_%s' % group_item
                        queryset = queryset.extra({convert_item_name: truncate_date})
                        group_field_list[index] = convert_item_name

                        order_field = order_field.replace(group_item, convert_item_name)
                        break

            queryset = queryset.values(*group_field_list)

            # Process something like Count(distinct item) or Count(item)
            aggregate_distinct = False
            if request.query_params.get(settings.AGGREGATE_DISTINCT, '0') == self.aggregate_distinct:
                aggregate_distinct = True

            # Process aggregate function
            kwargs = {self.search_type_map[aggregate_search_type]:\
                      getattr(django.db.models, self.search_type_map[aggregate_search_type].capitalize())(aggregate_search_field_list[0], distinct=aggregate_distinct)}

            queryset = queryset.annotate(**kwargs)

            # Process for order
            if order_field:
                order_field_list = order_field.split(settings.ORDERING_PARAM_DELIMITER)

                queryset = queryset.order_by(*order_field_list)

            # Process for limit,offset
            if self.pagination_class:
                #_pagination = pagination.LuPagination()
                _pagination = self.pagination_class()
                queryset = _pagination.paginate_queryset(queryset, request)

                if queryset is not None:
                    return _pagination.get_paginated_response(queryset)

            return Response(data=queryset)


        # For search process
        if request.query_params.get(settings.SEARCH_KEY):
            _lu_key = request.query_params.get(settings.SEARCH_KEY)
            lu_keys = _lu_key.replace(settings.SEARCH_KEY_DELIMITER, ' ').split()

            _lu_type = request.query_params.get(settings.SEARCH_TYPE, self.SEARCH_TYPE.contain)
            lu_types = _lu_type.replace(settings.SEARCH_TYPE_DELIMITER, ' ').split()

            if len(lu_types) != len(lu_keys):
                return LuResponse(code = status.LU_4007_INVALID_PARAM,
                         message = 'The number of `lu_search_field` should euqal the number of `lu_search_type`!')

            common_search_word_list = request.query_params.get(settings.SEARCH_PARAM, '').split(settings.SEARCH_PARAM_DELIMITER)

            if len(common_search_word_list) < len(lu_types):
                return LuResponse(code = status.LU_4007_INVALID_PARAM,
                         message = 'The number of `lu_search_word` should not less than %d' % len(lu_types))

            self.search_fields = ()
            self.search_words = ()

            for index, lu_key in enumerate(lu_keys):
                try:
                    prefix = self.search_type_map[lu_types[index]]
                except:
                    prefix = ''

                if lu_types[index] == self.SEARCH_TYPE._in:
                    # SQL IN: better performance for the string re
                    kwargs = {'%s__in' % lu_key: common_search_word_list[index].split(settings.SEARCH_PARAM_IN_DELIMITER)}
                    queryset = queryset.filter(**kwargs).distinct()
                    self.queryset = queryset
                    continue

                if lu_types[index] == self.SEARCH_TYPE._not_in:
                    # SQL NOT IN: better performance for the string re
                    kwargs = {'%s__in' % lu_key: common_search_word_list[index].split(settings.SEARCH_PARAM_NOTIN_DELIMITER)}
                    queryset = queryset.exclude(**kwargs).distinct()
                    self.queryset = queryset
                    continue

                key = prefix + lu_key
                self.search_fields += (key,)
                self.search_words += (common_search_word_list[index],)
        else:
            # if not specify search fields, use all instead
            search_fields = []
            for field in self.serializer_class.Meta.model._meta.fields:
                search_fields.append(str(field).split('.')[-1])

            self.search_fields = tuple(search_fields)

        response = super(LuModelViewSet, self).list(request, *args, **kwargs)

        # Here we provide ordering function for the method field in serializer
        # It's not a good practice to use in this way.
        # Suggest user leverage cache or other way for the method field order
        # for big data
        #if request.query_params.get(settings.ORDERING_PARAM, ''):
        #    order_field = request.query_params.get(settings.ORDERING_PARAM)
        #    order_type = True if order_field[0] == '-' else False

        #    if order_type:
        #        order_field = order_field[1:]

        #    if order_field in self.serializer_class._declared_fields.keys():
        #        response.data['data'] = sorted(response.data['data'], reverse=order_type, \
        #                                   key=itemgetter(order_field))

        return response

    def retrieve(self, request, *args, **kwargs):
        """
        HTTP GET item entry
        """
        return super(LuModelViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        HTTP POST item entry
        """
        # Check if do SQL injection first
        sql = request.data.get(settings.SQL_TEXT, '')

        if sql:
            sql_param = request.data.get(settings.SQL_PARAM, [])
            sql_param = [item.strip() for item in sql_param.split(',')] if sql_param else sql_param
            allow_sql = self.conf.sql_injection_allow
            map_sql = self.conf.sql_injection_map

            data = LuSQL(self.queryset._db, sql, sql_param, allow_sql, map_sql).execute()

            return LuResponse(data=data)

        if self.conf.enable_join_multiple_key_value_pair:
            data = self.get_body_data(request)

            # Join multiple key with delimiter
            for key in data:
                value = data.getlist(key)
                if len(value) > 1:
                    data[key] = self.conf.join_multiple_key_value_pair_delimiter.join(value)

            request = self.set_body_data(request, data)

        if not self.conf.enable_reversion_post:
            return super(LuModelViewSet, self).create(request, *args, **kwargs)
        else:
            with revisions.create_revision():
                resp = super(LuModelViewSet, self).create(request, *args, **kwargs)

                # Set metadata for reversion
                revisions.set_user(request.user)
                revisions.set_comment("[POST] Called from Lucommon Framework")

            return resp

    def update(self, request, *args, **kwargs):
        """
        HTTP PUT item entry
        """
        if self.conf.enable_join_multiple_key_value_pair:
            data = self.get_body_data(request)

            # Join multiple key with delimiter
            for key in data:
                value = data.getlist(key)
                if len(value) > 1:
                    data[key] = self.conf.join_multiple_key_value_pair_delimiter.join(value)

            request = self.set_body_data(request, data)

        if not self.conf.enable_reversion_update:
            return super(LuModelViewSet, self).update(request, *args, **kwargs)
        else:
            with revisions.create_revision():
                resp = super(LuModelViewSet, self).update(request, *args, **kwargs)

                # Set metadata for reversion
                revisions.set_user(request.user)
                revisions.set_comment("[UPDATE] Called from Lucommon Framework")

            return resp

    def partial_update(self, request, *args, **kwargs):
        """
        HTTP PATCH item entry
        """
        if not self.conf.enable_reversion_partial_update:
            return super(LuModelViewSet, self).partial_update(request, *args, **kwargs)
        else:
            with revisions.create_revision():
                resp = super(LuModelViewSet, self).partial_update(request, *args, **kwargs)

                # Set metadata for reversion
                revisions.set_user(request.user)
                revisions.set_comment("[PATCH] Called from Lucommon Framework")

            return resp

    def destroy(self, request, *args, **kwargs):
        """
        HTTP DELETE item entry
        """
        if not self.conf.enable_reversion_delete:
            return super(LuModelViewSet, self).destroy(request, *args, **kwargs)
        else:
            with revisions.create_revision():
                resp = super(LuModelViewSet, self).destroy(request, *args, **kwargs)

                # Set metadata for reversion
                revisions.set_user(request.user)
                revisions.set_comment("[DELETE] Called from Lucommon Framework")

            return resp

    def get_body_data(self, request):
        """
        Get data from body
        Usually, User in view could leverage get_body_data/set_body_data pair to change
        body data

        lucommon provide get_body_data/set_body_data pairs, as request.data is immutable
        """
        return request.data.copy()

    def set_body_data(self, request, data):
        """
        Set body data
        """
        request._full_data = data

        return request

    def get_query_params(self, request):
        """
        Get data from query params
        Usually, user in view could leverage get_query_params/set_query_params pair to change
        query params

        lucommon provide get_query_params/set_query_params pairs, as request.query_params is immutable
        """
        return request.query_params.copy()

    def set_query_params(self, request, query_params):
        """
        Set query params
        """
        request._request.GET = query_params

        return request




