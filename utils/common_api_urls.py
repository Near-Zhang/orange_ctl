from django.urls import re_path
from importlib import import_module

def geturlpatterns(plugin,*args):
    mod = import_module(plugin + '.views')
    extend_urlpatterns = []
    if not args:
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
    else:
        for i in args:
            view_class = getattr(mod,i.replace("-","_"))
            item = re_path(r'^%s/$'%i, view_class.as_view())
            extend_urlpatterns.append(item)
    return extend_urlpatterns