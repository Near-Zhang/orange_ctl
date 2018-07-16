import os
from django.urls import path,re_path,include
from utils.common_api_urls import geturlpatterns

urlpatterns = [ ]

plugin = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]
extend_urlpatterns = geturlpatterns(plugin)
urlpatterns.extend(extend_urlpatterns)
