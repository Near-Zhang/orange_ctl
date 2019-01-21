from django.urls import path, include
from .base_view import BaseView
from .exceptions import *

urlpatterns = [
    path(r'status/',include('status.urls')),
    path(r'divide/',include('divide.urls')),
    path(r'redirect/',include('redirect.urls')),
    path(r'upstream/',include('upstream.urls')),
    path(r'rewrite/',include('rewrite.urls')),
    path(r'mirror/',include('mirror.urls')),
    path(r'ssl/',include('ssl.urls'))
]


def handler404(request):
    try:
        raise PageNotFind
    except CustomException as e:
        BaseView().exception_to_response(e)


def handler500(request):
    try:
        raise InternalError
    except CustomException as e:
        BaseView().exception_to_response(e)
