from django.urls import path
from importlib import import_module


def get_url_patterns(plugin, part=False):
    mod = import_module(plugin + '.views')
    if not part:
        # 使用所有默认路由
        extend_urlpatterns = [
            path(r'enable/', mod.EnableView.as_view()),
            path(r'config/', mod.ConfigView.as_view()),
            path(r'fetch-config/', mod.FetchConfigView.as_view()),
            path(r'sync/', mod.SyncView.as_view()),
            path(r'selectors/', mod.SelectorsView.as_view()),
            path(r'selectors/order/', mod.SelectorsOrderView.as_view()),
            path(r'rules/', mod.RulesView.as_view()),
            path(r'rules/order/', mod.RulesOrderView.as_view()),
        ]
    else:
        # 使用部分路由
        extend_urlpatterns = [
            path(r'enable/', mod.EnableView.as_view()),
            path(r'config/', mod.ConfigView.as_view()),
            path(r'fetch-config/', mod.FetchConfigView.as_view()),
            path(r'sync/', mod.SyncView.as_view())
        ]

    return extend_urlpatterns
