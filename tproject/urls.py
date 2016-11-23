from django.conf.urls import url

from tproject.views import (
    ComponentViewSet,
    ProjectViewSet,
    RequirementTypeViewSet,
)


"""
Lucommon didn't use the Router class to register url,
Actually we set urls explicitly, one point is to control
what method we want to expose clearly.

By default, we set CURD and patch update. Please modify according
to your project
"""

urlpatterns = [
    url(r'^components/$', ComponentViewSet.as_view({'get':'list',
                                        'post': 'create'})),
    url(r'^components/(?P<pk>[0-9]+)$', ComponentViewSet.as_view({'get':'retrieve',
                                                      'put': 'update',
                                                      'patch': 'partial_update',
                                                      'delete': 'destroy'})),
    url(r'^components/(?P<pk>[0-9]+)/history$', ComponentViewSet.as_view({'get':'history'})),

    url(r'^projects/$', ProjectViewSet.as_view({'get':'list',
                                        'post': 'create'})),
    url(r'^projects/(?P<pk>[0-9]+)$', ProjectViewSet.as_view({'get':'retrieve',
                                                      'put': 'update',
                                                      'patch': 'partial_update',
                                                      'delete': 'destroy'})),
    url(r'^projects/(?P<pk>[0-9]+)/history$', ProjectViewSet.as_view({'get':'history'})),

    url(r'^requirementtypes/$', RequirementTypeViewSet.as_view({'get':'list',
                                        'post': 'create'})),
    url(r'^requirementtypes/(?P<pk>[0-9]+)$', RequirementTypeViewSet.as_view({'get':'retrieve',
                                                      'put': 'update',
                                                      'patch': 'partial_update',
                                                      'delete': 'destroy'})),
    url(r'^requirementtypes/(?P<pk>[0-9]+)/history$', RequirementTypeViewSet.as_view({'get':'history'})),

]


