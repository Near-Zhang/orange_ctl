from utils.baseview import Baseview
import time

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
            if enable == 1:
                node_ip_list = []
                for n in self.enable_nodes_qset:
                    node_ip_list.append(n.ip)
                if node_ip in node_ip_list:
                    msg = "Node %s is already enable." % node_ip
                else:
                    for p in self.plugins_list:
                        if p == "stat":continue
                        sync_dict = self.orange_sync_dict(p,node_ip=node_ip)
                        if not sync_dict["success"]:
                            msg = "faild to sync Node %s %s." %(node_ip,p)
                            return self.json_response(False, msg=msg)
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
        if nd:
            for node in self.enable_nodes_qset:
                if nd == node.ip:
                    url = self.compose_url('/stat/status', node=node.ip)
                    dict = self.orange_get_dict(url)
                    return self.json_response(**dict)
            msg = "node %s is not exist!" %nd
            return self.json_response(False, msg=msg)
        else:
            data = {
                "total_count":0,
                "request_2xx":0,
                "request_3xx":0,
                "request_4xx":0,
                "request_5xx":0
            }
            for node in self.enable_nodes_qset:
                url = self.compose_url('/stat/status', node=node.ip)
                dict = self.orange_get_dict(url)
                if dict['success']:
                    for i in data:
                        data[i] += dict["data"][i]
                else:
                    return self.json_response(**dict)
            data["timestamp"] = int(time.time())
            return self.json_response(True,data=data)

class clear(Baseview):
    """清空共享字典中的所有统计数据"""
    def post(self,request):
        error_dict = False
        error_node_list = []
        for node in self.enable_nodes_qset:
            url = self.compose_url('/stat/clear', node=node.ip)
            dict = self.orange_post_dict(url, None)
            if not dict['success']:
                error_node_list.append(node.ip)
        if error_dict:
            self.json_response(False,error_node_list)
        else:
            return self.json_response(**dict)

class node_sync(Baseview):
    """更新指定节点的所有插件"""
    def post(self,request):
        node_ip = request.POST.get('node')
        try:
            for p in self.plugins_list:
                if p == "stat":continue
                sync_dict = self.orange_sync_dict(p,node_ip=node_ip)
                if not sync_dict["success"]:
                    msg = "faild to sync Node %s %s." %(node_ip,p)
                    return self.json_response(False, msg=msg)
            msg = "succeed to sync Node %s." %(node_ip)
            return self.json_response(True, msg=msg)
        except:
            msg = "faild to sync Node %s." % node_ip
            return self.json_response(False, msg=msg)





