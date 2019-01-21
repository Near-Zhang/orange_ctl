from .base_view import BaseView
from orange_ctl.exceptions import CustomException
from orange_ctl.exceptions import RequestParamsError


class BaseEnableView(BaseView):
    """
    开启/关闭插件，设置数据库后，各节点同步最新插件配置
    """

    def post(self, request):
        try:
            # 请求设置
            request_params = self.get_params_dict(request)
            enable_opts = ['enable']
            enable_opts_dict = self.extract_opts(request_params, enable_opts)

            url = self.compose_orange_url('/'+self._plugin+'/enable')
            response = self.request_orange_api('post', url, data=enable_opts_dict)

            # 请求同步
            self.concurrent_sync_orange()

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class BaseConfigView(BaseView):
    """
    获取各节点同步的插件配置
    """

    def get(self, request):
        try:
            # 请求查询
            uri = '/'+self._plugin+'/config'
            response = self.concurrent_query_orange(uri, 'get')

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class BaseFetchConfigView(BaseView):
    """
    获取数据库的插件配置
    """

    def get(self, request):
        try:
            # 请求查询
            url = self.compose_orange_url('/'+self._plugin+'/fetch_config')
            response = self.request_orange_api('get', url)

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class BaseSyncView(BaseView):
    """
    同步数据库中的插件相关配置到共享字典
    """

    def post(self, request):
        try:
            # 请求同步
            response = self.concurrent_sync_orange()

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class BaseSelectorsView(BaseView):
    """
    选择器的增、删、改、查，除了查以外，均为设置数据库后，各节点同步最新插件配置
    """

    def get(self,request):
        try:
            # 请求查询
            uri = '/' + self._plugin + '/selectors'
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
                opts = ['selector']
            elif action == 'update':
                method = 'put'
                opts = ['selector']
            elif action == 'delete':
                method = 'delete'
                opts = ['selector_id']
            else:
                raise RequestParamsError(opt='action', invalid=True)

            opts_dict = self.extract_opts(request_params, opts)
            url = self.compose_orange_url('/' + self._plugin + '/selectors')
            response = self.request_orange_api(method, url, data=opts_dict)

            # 请求同步
            self.concurrent_sync_orange()

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class BaseSelectorsOrderView(BaseView):
    """
    修改选择器的顺序，设置数据库后，各节点同步最新插件配置
    后端体现是修改 meta 记录的 value.selectors 值
    """

    def post(self,request):
        try:
            # 请求设置
            request_params = self.get_params_dict(request)
            params_opts = ['order']
            params_opts_dict = self.extract_opts(request_params, params_opts)
            url = self.compose_orange_url('/' + self._plugin + '/selectors/order')

            response = self.request_orange_api('post', url, data=params_opts_dict)

            # 请求同步
            self.concurrent_sync_orange()

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class BaseRulesView(BaseView):
    """
    选择器中规则的增、删、改、查，除了查以外，均为设置数据库后，各节点同步最新插件配置
    """

    def get(self,request):
        try:
            # 请求查询
            request_params = self.get_params_dict(request)
            params_opts = ['selector_id']
            params_opts_dict = self.extract_opts(request_params, params_opts)

            uri = '/' + self._plugin + '/selectors/' + params_opts_dict['selector_id'] + '/rules'
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
                opts = ['rule', 'selector_id']
            elif action == 'update':
                method = 'put'
                opts = ['rule', 'selector_id']
            elif action == 'delete':
                method = 'delete'
                opts = ['rule_id', 'selector_id']
            else:
                raise RequestParamsError(opt='action', invalid=True)

            opts_dict = self.extract_opts(request_params, opts)
            selector_id = opts_dict.pop('selector_id')
            url = self.compose_orange_url('/' + self._plugin + '/selectors/' + selector_id +'/rules')
            response = self.request_orange_api(method, url, data=opts_dict)

            # 请求同步
            self.concurrent_sync_orange()

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)


class BaseRulesOrder(BaseView):
    """
    修改选择器中规则的顺序，设置数据库后，各节点同步最新插件配置
    后端体现是修改 selector 记录的 value.rules 值
    """

    def post(self, request):
        try:
            # 请求设置
            request_params = self.get_params_dict(request)
            params_opts = ['selector_id', 'order']
            params_opts_dict = self.extract_opts(request_params, params_opts)
            selector_id = params_opts_dict.pop('selector_id')
            url = self.compose_orange_url('/' + self._plugin + '/selectors/' + selector_id + '/rules/order')

            response = self.request_orange_api('post', url, data=params_opts_dict)

            # 请求同步
            self.concurrent_sync_orange()

            return self.standard_response(response)

        except CustomException as e:
            return self.exception_to_response(e)
