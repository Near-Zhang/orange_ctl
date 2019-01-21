import os
from orange_ctl.common_urls import get_url_patterns

urlpatterns = []

plugin = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]
extend_urlpatterns = get_url_patterns(plugin)
urlpatterns.extend(extend_urlpatterns)

