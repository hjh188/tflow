from tweb.serializers import (
    WebSourceSerializer,
)

from tweb.models import (
    WebSource,
)

from tweb.confs import (
    WebSourceConf,
)

from tweb.filters import (
    WebSourceFilter,
)

from lucommon import (
    viewsets,
)

from lucommon.response import LuResponse
from lucommon.logger import lu_logger

from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from lucommon.sql import LuSQL
from tuser.confs import UserConf

import json

"""
Write less, do more

* By viewsets.ModelViewSet, we can write restful API easily.
Usually, it's necessary to write CRUD operation in the viewset,
it's enough for common scenario. However, we can override
these functions(`list`, `create`, `retrieve`, `update`,
`partial_update`, `destroy`) for more detail control.

Example for HTTP GET:

def retrieve(self, request, *args, **kwargs):
    #`args` indicate the path without ?P(item) in urls route
    #`kwargs` indicate the param in ?P(item) in urls route
    do_something_before()
    response = super(viewsets.ModelViewSet, self).retrieve(request, *args, **kwargs)
    do_something_after()
    return response

* API docs(http://django-rest-swagger.readthedocs.org/en/latest/yaml.html)
Use the YAML Docstring for API docs

"""

def load_menu(view, request):
    # Load user self menu setting if has or load the default
    menu = LuSQL(UserConf.db, 'get_menu', [request.user.username], UserConf.sql_injection_allow, UserConf.sql_injection_map).execute()

    user_sidebar_menu_top_tag = json.loads(menu[0]['sidebar_menu_top']) if menu[0]['sidebar_menu_top'] else view.conf.default_sidebar_menu_top
    user_sidebar_menu_top = []

    for item in user_sidebar_menu_top_tag:
        user_sidebar_menu_top.append(view.conf.sidebar_menu_top_map[item])

    user_sidebar_menu_bottom_tag = json.loads(menu[0]['sidebar_menu_bottom']) if menu[0]['sidebar_menu_bottom'] else view.conf.default_sidebar_menu_bottom
    user_sidebar_menu_bottom = []

    for item in user_sidebar_menu_bottom_tag:
        user_sidebar_menu_bottom.append(view.conf.sidebar_menu_bottom_map[item])

    return (user_sidebar_menu_top, user_sidebar_menu_bottom)


class WebSourceViewSet(viewsets.LuModelViewSet):
    """
    ViewSet for WebSource operation
    """
    # Query set
    queryset = WebSource.objects.using(WebSourceConf.db).all()

    # Serializer class
    serializer_class = WebSourceSerializer

    # Filter class
    filter_class = WebSourceFilter

    # Conf class
    conf = WebSourceConf

    # APP name
    app = "tweb"

    # Model name
    model = "WebSource"

    def perform_create(self, serializer):
        """
        Keep this function for POST db select
        """
        serializer.save(using=WebSourceConf.db)

    def get_queryset(self):
        # Add whatever to filter the response if you want
        return WebSource.objects.using(WebSourceConf.db).all()


    def list(self, request, *args, **kwargs):
        """
        HTTP GET list entry
        """
        return super(WebSourceViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        HTTP GET item entry
        """
        return super(WebSourceViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        HTTP POST item entry
        """
        return super(WebSourceViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        HTTP PUT item entry
        """
        return super(WebSourceViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        HTTP PATCH item entry
        """
        return super(WebSourceViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        HTTP DELETE item entry
        """
        return super(WebSourceViewSet, self).destroy(request, *args, **kwargs)

    def get_login(self, request, *args, **kwargs):
        """
        Login page
        """
        logout(request)

        return render(request, 'login.html', dict({'next': request.query_params.get('next')}, **self.conf.base_resp_context))

    def post_login(self, request, *args, **kwargs):
        """
        Login Form
        """
        logout(request)

        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = request.query_params.get('next') if request.query_params.get('next') else 'index'
                return HttpResponseRedirect(next_page)

        return render(request, 'login.html', dict({'next': request.query_params.get('next')}, **self.conf.base_resp_context))

    def index(self, request, *args, **kwargs):
        """
        Index page
        """
        menu = load_menu(self, request)

        self.conf.base_resp_context['sidebar_menu_top'] = menu[0]
        self.conf.base_resp_context['sidebar_menu_bottom'] = menu[1]

        return render(request, 'index.html', self.conf.base_resp_context)


