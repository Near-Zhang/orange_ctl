import os
from orange_ctl.common_views import *

# 获取 app 名，即插件名
plugin = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]


class EnableView(BaseEnableView):
    @property
    def _plugin(self):
        return plugin


class ConfigView(BaseConfigView):
    @property
    def _plugin(self):
        return plugin


class FetchConfigView(BaseFetchConfigView):
    @property
    def _plugin(self):
        return plugin


class SyncView(BaseSyncView):
    @property
    def _plugin(self):
        return plugin


class SelectorsView(BaseSelectorsView):
    @property
    def _plugin(self):
        return plugin


class SelectorsOrderView(BaseSelectorsOrderView):
    @property
    def _plugin(self):
        return plugin


class RulesView(BaseRulesView):
    @property
    def _plugin(self):
        return plugin


class RulesOrderView(BaseRulesOrder):
    @property
    def _plugin(self):
        return plugin
