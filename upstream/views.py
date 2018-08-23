import os
from utils.common_api_views import *

plugin = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]

class enable(Base_enable):
    _plugin = plugin

class config(Base_config):
    _plugin = plugin

class fetch_config(Base_fetch_config):
    _plugin = plugin

class sync(Base_sync):
    _plugin = plugin

class upstreams(Baseview):
    _plugin = plugin

    def get(self,request):
        """获取共享字典中的配置"""
        main_url = self.compose_url('/upstream/upstreams')
        main_node_dict = self.orange_get_dict(main_url)
        for node in self.enable_nodes_qset[1:]:
            url = self.compose_url('/upstream/upstreams', node=node.ip)
            dict = self.orange_get_dict(url)
            if dict != main_node_dict:
                if dict['success']:
                    msg = "Node %s %s is not updated!" % (node.ip, self._plugin)
                    return self.json_response(False, msg=msg)
                else:
                    return self.json_response(**dict)
        return self.json_response(**main_node_dict)

    def post(self,request):
        action = request.POST.get('action')
        if action == 'create':
            data_item = ['upstream']
            handler = self.orange_post_dict
        elif action == 'delete':
            data_item = ['upstream_name']
            handler = self.orange_delete_dict
        elif action == 'update':
            data_item = ['upstream']
            handler = self.orange_put_dict
        else:
            msg = "The action %s is not avaliable! " %action
            return self.json_response(False, msg=msg)
        data = {}
        for k in data_item:
            data[k] = request.POST.get(k)
        url = self.compose_url('/upstream/upstreams')
        dict = handler(url, data)
        sync_dict = self.orange_sync_dict(self._plugin)
        if sync_dict['success']:
            return self.json_response(**dict)
        else:
            return self.json_response(**sync_dict)

class checker(Baseview):
    _plugin = plugin

    def get(self,request):
        """获取监控检查状态"""
        nd = request.GET.get('node')
        upstream_name = request.GET.get('upstream_name')
        base_url = '/upstream/checker'
        if upstream_name: base_url = '/upstream/checker?upstream_name=%s' %upstream_name
        if nd:
            for node in self.enable_nodes_qset:
                if nd == node.ip:
                    url = self.compose_url(base_url, node=node.ip)
                    dict = self.orange_get_dict(url)
                    return self.json_response(**dict)
            msg = "node %s is not exist!" % nd
            return self.json_response(False, msg=msg)
        else:
            data = {}
            for node in self.enable_nodes_qset:
                url = self.compose_url(base_url, node=node.ip)
                dict = self.orange_get_dict(url)
                if dict["success"]:
                    data[node.ip] = dict["data"]
                else:
                    data[node.ip] = dict["msg"]
            return self.json_response(True, data=data)