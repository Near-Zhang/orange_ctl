from django.urls import path,re_path,include
from .views import *

urlpatterns = [
    re_path(r'^nodes/$',nodes.as_view()),
    re_path(r'^stat/$',stat.as_view()),
    re_path(r'^clear/$',clear.as_view()),
    re_path(r'plugins/$',plugins.as_view()),
    re_path(r'node-sync/$',node_sync.as_view()),
]


