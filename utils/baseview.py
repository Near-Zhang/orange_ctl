from django.views import View
from django.http import JsonResponse
from django.conf import settings
from status.models import Nodes
import requests,base64

class Baseview(View):

    _auth_header = {
        "Authorization": base64.b64encode(b"api_username:api_password")
    }

    @property
    def all_nodes_qset(self):
        return Nodes.objects.all()

    @property
    def enable_nodes_qset(self):
        return Nodes.objects.filter(enable=1)

    @property
    def plugins_list(self):
        plugins_url = self.compose_url('/plugins')
        plugins_dict = self.orange_get_dict(plugins_url)
        return list(plugins_dict['data']['plugins'])

    def compose_url(self, uri, port='7777', node="master"):
        if node == "master":node = Nodes.objects.filter(enable=1).first().ip
        return "http://" + node + ':' + port + uri

    def json_response(self, success,data=None, msg=None):
        return JsonResponse(
            {
            "success": success,
            "data": data,
            "msg": msg
            }
        )

    def orange_get_dict(self,url):
        try:
            obj = requests.get(url, headers=self._auth_header).json()
            return obj
        except:
            return {
                "success": False,
                "msg": "GET: %s is not avaliable!" %url
            }

    def orange_post_dict(self,url,data):
        try:
            obj = requests.post(url, data=data ,headers=self._auth_header).json()
            return obj
        except:
            return {
                "success": False,
                "msg": "POST: %s is not avaliable!" %url
            }

    def orange_delete_dict(self,url,data):
        try:
            obj = requests.delete(url,data=data, headers=self._auth_header).json()
            return obj
        except:
            return {
                "success": False,
                "msg": "DELETE: %s is not avaliable!" %url
            }

    def orange_put_dict(self, url, data):
        try:
            obj = requests.put(url, data=data, headers=self._auth_header).json()
            return obj
        except:
            return {
                "success": False,
                "msg": "PUT: %s is not avaliable!" % url
            }

    def orange_sync_dict(self,plugin,node_ip="all"):
        if node_ip == "all":
            error_dict = False
            error_node_list = []
            for node in self.enable_nodes_qset:
                url = self.compose_url('/'+plugin+'/sync', node=node.ip)
                dict = self.orange_post_dict(url, None)
                if not dict['success']:
                    error_node_list.append(node.ip)
            if error_dict:
                return {
                    "success": False,
                    "data":error_node_list
                }
            else:
                return dict
        else:
            url = self.compose_url('/' + plugin + '/sync', node=node_ip)
            dict = self.orange_post_dict(url, None)
            return dict

    def get(self,request):
        msg = "http method GET is not supported by this url"
        return self.json_response(False,msg=msg)

    def post(self,request):
        msg = "http method POST is not supported by this url"
        return self.json_response(False,msg=msg)
