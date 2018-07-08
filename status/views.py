from utils.baseview import Baseview

class nodes(Baseview):
    """从sqlite查询、修改所有节点和启用节点"""
    def get(self,request):
        active = int(request.GET.get('active','0'))
        if active:
            nodes_info = self.enable_nodes_qset.values('ip','location')
        else:
            nodes_info = self.all_nodes_qset.values('ip','location','enable')
        data = {'nodes' :list(nodes_info)}
        return self.json_response(True, data=data)

    def post(self,request):
        node_ip = request.POST.get('node')
        enable = int(request.POST.get('enable'))
        try:
            if enable:
                self.all_nodes_qset.filter(ip=node_ip).update(enable=1)
                msg = "succeed to enable Node %s." %node_ip
            else:
                self.all_nodes_qset.filter(ip=node_ip).update(enable=0)
                msg = "succeed to disable Node %s." % node_ip
            return self.json_response(True, msg=msg)
        except:
            msg = "faild to change Node %s." % node_ip
            return self.json_response(False, msg=msg)

class plugins(Baseview):
    """从共享字典查询所有插件的简要状态"""
    def get(self,request):
        main_url = self.compose_url('/plugins')
        main_node_dict = self.orange_get_dict(main_url)
        for node in self.enable_nodes_qset[1:]:
            url = self.compose_url('/plugins', node=node.ip)
            dict = self.orange_get_dict(url)
            if dict != main_node_dict:
                if dict['success']:
                    for plugin in main_node_dict['data']['plugins']:
                        if dict['data']['plugins'][plugin] != main_node_dict['data']['plugins'][plugin]:
                            msg = "node %s %s is not updated!" %(node.ip ,plugin)
                            return self.json_response(False, msg=msg)
                else:
                    return self.json_response(**dict)
        return self.json_response(**main_node_dict)

class stat(Baseview):
    """从共享字典查询指定节点的全据统计"""
    def get(self,request):
        nd = request.GET.get('node')
        for node in self.enable_nodes_qset:
            if nd == node.ip:
                url = self.compose_url('/stat/status', node=node.ip)
                dict = self.orange_get_dict(url)
                return self.json_response(**dict)
        msg = "node %s is not exist!" %nd
        return self.json_response(False, msg=msg)








