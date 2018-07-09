from utils.baseview import Baseview

class Base_enable(Baseview):
    """开启或者关闭插件，先修改数据库并更新共享字典"""
    _plugin = 'plugin'

    def post(self,request):
        data = request.POST
        url = self.compose_url('/'+self._plugin+'/enable')
        dict = self.orange_post_dict(url, data)
        sync_dict = self.orange_sync_dict(self._plugin)
        if sync_dict['success']:
            return self.json_response(**dict)
        else:
            return self.json_response(**sync_dict)

class Base_config(Baseview):
    """获取共享字典中的插件相关配置内容"""
    _plugin = 'plugin'

    def get(self,request):
        main_url = self.compose_url('/'+self._plugin+'/config')
        main_node_dict = self.orange_get_dict(main_url)
        for node in self.enable_nodes_qset[1:]:
            url = self.compose_url('/'+self._plugin+'/config', node=node.ip)
            dict = self.orange_get_dict(url)
            if dict != main_node_dict:
                if dict['success']:
                    msg = "Node %s %s is not updated!" %(node.ip,self._plugin)
                    return self.json_response(False, msg=msg)
                else:
                    return self.json_response(**dict)
        return self.json_response(**main_node_dict)

class Base_fetch_config(Baseview):
    """获取数据库中的插件相关配置内容"""
    _plugin = 'plugin'

    def get(self,request):
        url = self.compose_url('/'+self._plugin+'/fetch_config')
        dict = self.orange_get_dict(url)
        return self.json_response(**dict)

class Base_sync(Baseview):
    """同步数据库中的插件相关配置到共享字典"""
    _plugin = 'plugin'

    def post(self,request):
        dict = self.orange_sync_dict(self._plugin)
        return self.json_response(**dict)

class Base_selectors(Baseview):

    _plugin = 'plugin'

    def get(self,request):
        """获取共享字典中的插件、meta、selector配置内容"""
        main_url = self.compose_url('/'+self._plugin+'/selectors')
        main_node_dict = self.orange_get_dict(main_url)
        for node in self.enable_nodes_qset[1:]:
            url = self.compose_url('/'+self._plugin+'/selectors', node=node.ip)
            dict = self.orange_get_dict(url)
            if dict != main_node_dict:
                if dict['success']:
                    msg = "Node %s %s is not updated!" %(node.ip,self._plugin)
                    return self.json_response(False, msg=msg)
                else:
                    return self.json_response(**dict)
        return self.json_response(**main_node_dict)

    def post(self,request):
        """创建、删除、修改选择器，先修改数据库并更新共享字典"""
        action = request.POST.get('action')
        if action == 'create':
            data_item = ['selector']
            handler = self.orange_post_dict
        elif action == 'delete':
            data_item = ['selector_id']
            handler = self.orange_delete_dict
        elif action == 'update':
            data_item = ['selector']
            handler = self.orange_put_dict
        else:
            msg = "The action %s is not avaliable! " %action
            return self.json_response(False, msg=msg)
        data = {}
        for k in data_item:
            data[k] = request.POST.get(k)
        url = self.compose_url('/'+self._plugin+'/selectors')
        dict =handler(url,data)
        sync_dict = self.orange_sync_dict(self._plugin)
        if sync_dict['success']:
            return self.json_response(**dict)
        else:
            return self.json_response(**sync_dict)

class Base_selectors_order(Baseview):
    """修改选择器的数据，本质修改mysql中meta记录的value.selectors值，并更新共享字典"""
    _plugin = 'plugin'

    def post(self,request):
        data = request.POST
        url = self.compose_url('/' + self._plugin + '/selectors/order')
        dict = self.orange_put_dict(url, data)
        sync_dict = self.orange_sync_dict(self._plugin)
        if sync_dict['success']:
            return self.json_response(**dict)
        else:
            return self.json_response(**sync_dict)

class Base_rules(Baseview):

    _plugin = 'plugin'

    def get(self,request):
        """查询指定选择器中的规则，从共享字典中查询"""
        selector_id = request.GET.get('selector_id')
        main_url = self.compose_url('/' + self._plugin + '/selectors/' + selector_id + '/rules')
        main_node_dict = self.orange_get_dict(main_url)
        for node in self.enable_nodes_qset[1:]:
            url = self.compose_url('/' + self._plugin + '/selectors/' + selector_id + '/rules',node=node.ip)
            dict = self.orange_get_dict(url)
            if dict != main_node_dict:
                if dict['success']:
                    msg = "Node %s %s is not updated!" % (node.ip, self._plugin)
                    return self.json_response(False, msg=msg)
                else:
                    return self.json_response(**dict)
        return self.json_response(**main_node_dict)

    def post(self,request):
        """创建、删除、修改指定选择器中的规则，先修改数据库并更新共享字典"""
        action = request.POST.get('action')
        if action == 'create':
            data_item = ['rule']
            handler = self.orange_post_dict
        elif action == 'delete':
            data_item = ['rule_id']
            handler = self.orange_delete_dict
        elif action == 'update':
            data_item = ['rule']
            handler = self.orange_put_dict
        else:
            msg = "The action %s is not avaliable! " %action
            return self.json_response(False, msg=msg)
        data = {}
        for k in data_item:
            data[k] = request.POST.get(k)
        selector_id = request.POST.get('selector_id')
        url = self.compose_url('/'+self._plugin+'/selectors/'+selector_id+'/rules')
        dict = handler(url, data)
        sync_dict = self.orange_sync_dict(self._plugin)
        if sync_dict['success']:
            return self.json_response(**dict)
        else:
            return self.json_response(**sync_dict)

class Base_rules_order(Baseview):
    """修改选择器的数据，本质修改mysql中selector记录的value.rules值，并更新共享字典"""
    _plugin = 'plugin'

    def post(self, request):
        selector_id = request.POST.get('selector_id')
        data = {}
        data['order'] = request.POST.get('order')
        url = self.compose_url('/' + self._plugin + '/selectors/'+ selector_id +'/rules/order')
        dict = self.orange_put_dict(url, data)
        sync_dict = self.orange_sync_dict(self._plugin)
        if sync_dict['success']:
            return self.json_response(**dict)
        else:
            return self.json_response(**sync_dict)


