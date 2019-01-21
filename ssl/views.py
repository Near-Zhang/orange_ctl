import os
from orange_ctl.common_views import *
from orange_ctl.base_view import BaseView

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


class CertsView(BaseView):
    """
    证书的增、删、改、查，除了查以外，均为设置数据库后，各节点同步最新插件配置
    """
    @property
    def _plugin(self):
        return plugin

    def get(self, request):
        try:
            # 请求查询
            uri = '/' + self._plugin + '/certs'
            response = self.concurrent_query_orange(uri, 'get')

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)

    def post(self,request):
        try:
            # 请求设置
            request_params = self.get_params_dict(request)
            action_opts = ['action']
            action_opts_dict = self.extract_opts(request_params, action_opts)

            action = action_opts_dict['action']
            if action == 'create':
                method = 'post'
                opts = ['cert']
            elif action == 'update':
                method = 'put'
                opts = ['cert']
            elif action == 'delete':
                method = 'delete'
                opts = ['cert_name']
            else:
                raise RequestParamsError(opt='action', invalid=True)

            opts_dict = self.extract_opts(request_params, opts)
            url = self.compose_orange_url('/' + self._plugin + '/certs')
            response = self.request_orange_api(method, url, data=opts_dict)

            # 请求同步
            self.concurrent_sync_orange()

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)