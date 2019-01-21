from orange_ctl.exceptions import *
from django.views import View
from django.http import JsonResponse
from status.models import Nodes
import base64
import requests
from requests.exceptions import RequestException
from django.http import QueryDict
from concurrent.futures import ThreadPoolExecutor


class BaseView(View):
    """
    基础视图类，提供返回响应的方法，以及限制非允许方法的请求，提取参数的方法
    """

    http_method_names = ['get', 'post', 'put', 'delete', 'options']

    @staticmethod
    def standard_response(data=None, code=200, message=None):
        """
        生成标准的 JsonResponse 对象
        :param data: dict, 数据
        :param code: int, 返回码
        :param message: str, 错误信息
        :return: JsonResponse object, json 响应对象
        """
        # 兼容当前的前端
        if code == 200:
            success = True
        else:
            success = False

        res_dict = {
            'success': success,
            'data': data,
            'message': message
        }
        return JsonResponse(res_dict)

    def dispatch(self, request, *args, **kwargs):
        """
        根据请求的方法，分发视图函数
        :param request: request object, 请求
        :param args: tuple, 位置参数
        :param kwargs: dict, 关键字参数
        :return: Response object, 响应对象
        """
        try:
            if request.method.lower() in self.http_method_names:
                try:
                    handler = getattr(self, request.method.lower())
                except AttributeError:
                    raise MethodNotAllowed(request.method.lower(), request.path)
                else:
                    return handler(request, *args, **kwargs)
        except MethodNotAllowed as e:
            return self.exception_to_response(e)

    def exception_to_response(self, exception):
        """
        接收异常对象，转化为 json 响应对象并返回
        :param exception: Exception object, 异常对象
        :return: Response object, 响应对象
        """
        code = exception.code
        message = exception.__message__()
        return self.standard_response(code=code, message=message)

    @staticmethod
    def get_params_dict(request, nullable=False):
        """
        从请求中获取参数字典
        :param request: request object, 请求
        :param nullable: bool, 是否可为空
        :return: dict, 请求参数字典
        """
        if request.method == 'GET':
            request_params = request.GET
        else:
            request_params = QueryDict(request.body)

        if not request_params and not nullable:
            raise RequestParamsError(empty=True)

        return request_params

    @staticmethod
    def extract_opts(request_params, opts_list, necessary=True):
        """
        从参数中提取指定选项，返回字典
        :param request_params: dict, 请求参数字典
        :param opts_list: list, 参数名列表
        :param necessary: bool, 是否为必要参数
        :return: dict, 提取后的参数字典
        """
        extract_dict = {}
        for opt in opts_list:
            v = request_params.get(opt)
            if v is not None:
                extract_dict[opt] = v
            elif necessary:
                raise RequestParamsError(opt=opt)
        return extract_dict

    @property
    def _plugin(self):
        """
        子类不覆写基础类的 plugin，将报错
        :return: None
        """
        raise ValueError

    @staticmethod
    def compose_orange_url(uri, node=None):
        """
        拼接用于访问 orange 节点的 url
        :param uri: str， URI
        :param port: str, 断开
        :param node: str, 节点 ip，默认为 master
        :return:
        """
        if not node:
            node = Nodes.objects.filter(enable=True, master=True).first()
        return "http://" + node.ip + ':' + node.port + uri

    @staticmethod
    def request_orange_api(method, url, data=None):
        """
        请求 orange 节点获取字典化的响应
        :param method: str, 请求方法
        :param url: str, URL
        :param data: dict, 参数
        :return: dict, 响应
        """
        auth_header = {
            "Authorization": base64.b64encode(b"api_username:api_password")
        }

        try:
            request_func = getattr(requests, method)
            if method == 'get':
                response = request_func(url, params=data, headers=auth_header).json()
            else:
                response = request_func(url, data=data, headers=auth_header).json()

            if not response.get('success'):
                raise ResponseBackendError(method, url, response['msg'])

            return response

        except RequestException:
            raise RequestBackendError(method, url)

    def concurrent_query_orange(self, uri, method, data=None):
        """
        并发请求 orange 节点，获取指定配置
        :return:
        """
        # 获取节点对象
        future_list = []
        master_node = Nodes.objects.filter(enable=True, master=True).first()
        slave_node_obj_qs = Nodes.objects.filter(enable=True, master=False)

        with ThreadPoolExecutor(max_workers=4) as executor:
            # 提交 master 请求任务
            master_url = self.compose_orange_url(uri, node=master_node)
            master_future = executor.submit(self.request_orange_api, method, master_url, data)
            future_list.append(master_future)

            # 提交 slave 请求任务
            for slave_node in slave_node_obj_qs:
                slave_url = self.compose_orange_url(uri, node=slave_node)
                slave_future = executor.submit(self.request_orange_api, method, slave_url, data)
                slave_future.node = slave_node
                future_list.append(slave_future)

        last_result = None
        for future in future_list:
            result = future.result()
            if last_result:
                if result != last_result:
                    raise OrangeNodeNotUpdate(future.node.ip, future.port)
            last_result = result

        return last_result.get('data')

    def concurrent_sync_orange(self):
        """
        并发请求 orange 节点，使同步最新插件配置
        :return:
        """
        future_list = []
        node_obj_qs = Nodes.objects.filter(enable=True)
        uri = '/'+self._plugin+'/sync'

        with ThreadPoolExecutor(max_workers=4) as executor:
            for node in node_obj_qs:
                url = self.compose_orange_url(uri, node=node)
                future = executor.submit(self.request_orange_api, 'post', url)
                future_list.append(future)

        last_result = None
        for future in future_list:
            result = future.result()
            last_result = result

        return last_result.get('data')
