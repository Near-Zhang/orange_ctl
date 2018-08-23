import os
from .views import *
from django.urls import path,re_path,include
from utils.common_api_urls import geturlpatterns

urlpatterns = [
    re_path( r'^upstreams/$',upstreams.as_view()),
    re_path( r'^checker/$',checker.as_view())
    ]

plugin = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]
extend_urlpatterns = geturlpatterns(plugin,'enable','sync','config','fetch-config')
urlpatterns.extend(extend_urlpatterns)