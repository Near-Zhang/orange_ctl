from django.urls import re_path
from importlib import import_module

def geturlpatterns(plugin):
    mod = import_module(plugin + '.views')
    extend_urlpatterns = [
        re_path(r'^enable/$',mod.enable.as_view()),
        re_path(r'^config/$',mod.config.as_view()),
        re_path(r'^fetch-config/$',mod.fetch_config.as_view()),
        re_path(r'^sync/$', mod.sync.as_view()),
        re_path(r'^selectors/$', mod.selectors.as_view()),
        re_path(r'^selectors/order/$', mod.selectors_order.as_view()),
        re_path(r'^rules/$',mod.rules.as_view()),
        re_path(r'^rules/order/$', mod.rules_order.as_view()),
    ]
    return extend_urlpatterns