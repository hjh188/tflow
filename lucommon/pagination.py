#!/usr/bin/env python

from rest_framework import pagination
from rest_framework.response import Response

from lucommon import settings

class LuPagination(pagination.LimitOffsetPagination):
    """
    Custom for the pagnination output
    """
    limit_query_param = settings.LIMIT_FIELD
    offset_query_param = settings.OFFSET_FIELD
    default_limit = settings.DEFAULT_LIMIT
    max_limit = settings.MAX_LIMIT
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.count,
             },
            'data': data
        })

class LuPagination2(pagination.LimitOffsetPagination):
    """
    NO format for output
    """
    limit_query_param = settings.LIMIT_FIELD
    offset_query_param = settings.OFFSET_FIELD
    default_limit = settings.DEFAULT_LIMIT
    max_limit = settings.MAX_LIMIT


