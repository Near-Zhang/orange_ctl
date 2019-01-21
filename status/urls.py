from django.urls import path
from .views import *

urlpatterns = [
    path(r'nodes/', NodesView.as_view()),
    path(r'stat/', StatView.as_view()),
    path(r'plugins/', PluginsView.as_view()),
    path(r'node-sync/', NodeSyncView.as_view()),
]


