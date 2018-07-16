from django.urls import path,re_path,include
from utils.baseview import Baseview

urlpatterns = [
    path(r'status/',include('status.urls')),
    path(r'divide/',include('divide.urls')),
    path(r'redirect/',include('redirect.urls')),
    path(r'upstream/',include('upstream.urls')),
    path(r'rewrite/',include('rewrite.urls'))
]

def handler404(request):
    msg = "404:not found"
    res = Baseview.json_response(Baseview,False,msg=msg)
    res.status_code = 404
    return res

def handler500(request):
    msg = "500:server error"
    res = Baseview.json_response(Baseview,False, msg=msg)
    res.status_code = 500
    return res
