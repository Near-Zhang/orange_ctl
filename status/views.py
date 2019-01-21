from orange_ctl.base_view import BaseView
from orange_ctl.exceptions import *
from .models import Nodes
import time


class NodesView(BaseView):
    """
    节点的查询和启用/禁用
    """

    def get(self, request):
        node_obj_qs = Nodes.objects.all()
        node_list = []
        for node_obj in node_obj_qs:
            node_list.append(node_obj.serialize())

        return self.standard_response(node_list)

    def post(self,request):
        try:
            # 参数获取
            request_params = self.get_params_dict(request)
            params_opts = ['ip', 'port', 'enable']
            params_opts_dict = self.extract_opts(request_params, params_opts)

            enable = params_opts_dict.pop('enable')

            # 请求同步
            node_obj = Nodes.objects.get(**params_opts_dict)
            if enable:
                if node_obj.enable:
                    return self.standard_response()
                else:
                    plugins_url = self.compose_orange_url('/plugins')
                    plugins_response = self.request_orange_api('get', plugins_url)
                    for p in plugins_response['plugins']:
                        if p == "stat":
                            continue
                        sync_url = self.compose_orange_url('/'+self._plugin+'/sync',node=node_obj)
                        self.request_orange_api('get', sync_url)

            node_obj.enable = enable
            node_obj.save()
            return self.standard_response()

        except CustomException as e:
            return self.exception_to_response(e)


class PluginsView(BaseView):
    """
    查询所有插件的简要状态
    """

    def get(self,request):
        try:
            # 请求查询
            uri = '/plugins'
            response = self.concurrent_query_orange(uri, 'get')

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class StatView(BaseView):
    """
    从共享字典查询指定节点的全据统计
    """

    def get(self,request):
        try:
            data = {
                "total_count":0,
                "request_2xx":0,
                "request_3xx":0,
                "request_4xx":0,
                "request_5xx":0,
                "con_reading": 0,
                "con_writing": 0,
                "con_rw": 0,
                "con_active": 0,
                "con_idle": 0,
                "traffic_read": 0,
                "traffic_write": 0
            }

            node_obj_qs = Nodes.objects.all()
            for node_obj in node_obj_qs:
                url = self.compose_orange_url('/stat/status', node=node_obj)
                response = self.request_orange_api('get', url)
                for k in data:
                    data[k] += response["data"][k]
                data["timestamp"] = int(time.time())
                return self.standard_response(data)

        except CustomException as e:
            return self.exception_to_response(e)


class NodeSyncView(BaseView):
    """
    更新指定节点的所有插件
    """

    def post(self,request):
        try:
            # 参数获取
            request_params = self.get_params_dict(request)
            params_opts = ['ip', 'port']
            params_opts_dict = self.extract_opts(request_params, params_opts)

            # 请求同步
            node_obj = Nodes.objects.get(**params_opts_dict)
            plugins_url = self.compose_orange_url('/plugins')
            plugins_response = self.request_orange_api('get', plugins_url)
            for p in plugins_response['plugins']:
                if p == "stat":
                    continue
                sync_url = self.compose_orange_url('/' + self._plugin + '/sync', node=node_obj)
                self.request_orange_api('get', sync_url)

            return self.standard_response()

        except CustomException as e:
            return self.exception_to_response(e)





