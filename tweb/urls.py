from django.conf.urls import url

from tweb.views import (
    WebSourceViewSet,
)


"""
Lucommon didn't use the Router class to register url,
Actually we set urls explicitly, one point is to control
what method we want to expose clearly.

By default, we set CURD and patch update. Please modify according
to your project
"""

urlpatterns = [
    url(r'^websources/$', WebSourceViewSet.as_view({'get':'list',
                                        'post': 'create'})),
    url(r'^websources/(?P<pk>[0-9]+)$', WebSourceViewSet.as_view({'get':'retrieve',
                                                      'put': 'update',
                                                      'patch': 'partial_update',
                                                      'delete': 'destroy'})),
    url(r'^login', WebSourceViewSet.as_view({'get':'get_login', 'post':'post_login'})),
    url(r'^index', WebSourceViewSet.as_view({'get':'index'})),
    url(r'^project/dashboard', WebSourceViewSet.as_view({'get':'project_dashboard'})),
    url(r'^project/all', WebSourceViewSet.as_view({'get':'project_all'})),

]


