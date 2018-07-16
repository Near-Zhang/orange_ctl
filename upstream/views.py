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