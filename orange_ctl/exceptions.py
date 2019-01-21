class CustomException(Exception):
    """
    自定义异常类，修改了打印时的显示方式
    """

    def __message__(self):
        exception_message = self.args[0]
        exception_class = self.__class__.__name__
        return '%s: %s' %(exception_class, exception_message)


class PageNotFind(CustomException):
    """
    无法找到页面
    """
    def __init__(self, path):
        self.code = 404
        exception_message = 'path %s is not find' % path
        super().__init__(exception_message)


class InternalError(CustomException):
    """
    服务内部逻辑错误
    """
    def __init__(self):
        self.code = 500
        exception_message = 'there was an internal error'
        super().__init__(exception_message)


class MethodNotAllowed(CustomException):
    """
    请求的方法不被允许
    """
    def __init__(self, method, path):
        self.code = 405
        exception_message = '%s method is not allowed by %s path' % (method, path)
        super().__init__(exception_message)


class LoginFailed(CustomException):
    """
    登录失败
    """
    def __init__(self):
        self.code = 403
        exception_message = 'user does not exist or password error'
        super().__init__(exception_message)


class CredenceInvalid(CustomException):
    """
    凭证校验无效
    """
    def __init__(self, empty=False):
        self.code = 403
        exception_message = 'the user or token in the cookie is invalid'
        if empty:
            exception_message = 'the user or token in the cookie is required'
        super().__init__(exception_message)


class PasswordInvalid(CustomException):
    def __init__(self, message):
        self.code = 400
        exception_message = message
        super().__init__(exception_message)


class RequestParamsError(CustomException):
    """
    从请求中提取的参数有错误
    """
    def __init__(self, empty=False, opt=None, invalid=None):
        self.code = 400
        if empty:
            exception_message = 'request params is empty'
        elif opt and not invalid:
            exception_message = 'the %s of request params is missing or none' % opt
        elif opt and invalid:
            exception_message = 'the %s of request params is not in range' % opt
        else:
            exception_message = 'request params is not a standard json'
        super().__init__(exception_message)


class ObjectNotExist(CustomException):
    """
    模型中不存在查找的对象
    """
    def __init__(self, model):
        self.code = 404
        exception_message = 'objects does not exist in the model %s' % model
        super().__init__(exception_message)


class DatabaseError(CustomException):
    """
    数据库进行对象保存操作时的错误
    """
    def __init__(self, msg, model):
        self.code = 409
        exception_message = '%s in the model %s' % (msg.lower(), model)
        super().__init__(exception_message)


class RequestBackendError(CustomException):
    """
    对后端请求 api 错误
    """
    def __init__(self, method, url):
        self.code = 502
        exception_message = 'the response of %s %s is not available' % (method, url)
        super().__init__(exception_message)


class ResponseBackendError(CustomException):
    """
    对后端请求 api 返回的响应错误
    """
    def __init__(self, method, url, message):
        self.code = 500
        exception_message = 'the response of %s %s is %s' % (method, url, message)
        super().__init__(exception_message)


class OrangeNodeNotUpdate(CustomException):
    """
    对后端节点配置不一致
    """
    def __init__(self, ip, port):
        self.code = 500
        exception_message = 'the node %s:%s of backend is inconsistent' % (ip, port)
        super().__init__(exception_message)