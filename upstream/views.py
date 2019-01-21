import os
from orange_ctl.common_views import *
from orange_ctl.base_view import BaseView
from status.models import Nodes

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


class UpstreamsView(BaseView):
    """
    上游的增删改查
    """
    @property
    def _plugin(self):
        return plugin

    def get(self, request):
        try:
            # 请求查询
            uri = '/' + self._plugin + '/upstreams'
            response = self.concurrent_query_orange(uri, 'get')

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)

    def post(self,request):
        try:
            request_params = self.get_params_dict(request)
            action_opts = ['action']
            action_opts_dict = self.extract_opts(request_params, action_opts)

            action = action_opts_dict['action']
            if action == 'create':
                method = 'post'
                opts = ['upstream']
            elif action == 'update':
                method = 'put'
                opts = ['upstream']
            elif action == 'delete':
                method = 'delete'
                opts = ['upstream_name']
            else:
                raise RequestParamsError(opt='action', invalid=True)

            opts_dict = self.extract_opts(request_params, opts)
            url = self.compose_orange_url('/' + self._plugin + '/upstreams')
            response = self.request_orange_api(method, url, data=opts_dict)

            # 请求同步
            self.concurrent_sync_orange()

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class CheckerView(BaseView):
    """
    检查器状态查询
    """
    @property
    def _plugin(self):
        return plugin

    def get(self,request):
        try:
            request_params = self.get_params_dict(request, nullable=True)
            params_opts = ['upstream_name']
            params_opts_dict = self.extract_opts(request_params, params_opts, necessary=False)

            nd = request.GET.get('node')
            node_obj_qs = Nodes.objects.all()
            if nd:
                for node in node_obj_qs:
                    if nd == node.ip:
                        url = self.compose_orange_url('/upstream/checker', node=node)
                        response = self.request_orange_api('get', url, data=params_opts_dict)
                        return self.standard_response(response)
                msg = "node %s is not exist!" % nd
                return self.standard_response(code=404, message=msg)
            else:
                data = {}
                for node in node_obj_qs:
                    url = self.compose_orange_url('/upstream/checker', node=node)
                    response = self.request_orange_api('get', url, data=params_opts_dict)
                    data[node.ip] = response.get('data')
                return self.standard_response(data)

        except CustomException as e:
            return self.exception_to_response(e)