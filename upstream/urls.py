import os
from django.urls import path
from orange_ctl.common_urls import get_url_patterns
from .views import UpstreamsView, CheckerView

urlpatterns = [
    path( r'upstreams/', UpstreamsView.as_view()),
    path( r'checker/', CheckerView.as_view())
    ]

plugin = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]
extend_urlpatterns = get_url_patterns(plugin, part=True)
urlpatterns.extend(extend_urlpatterns)