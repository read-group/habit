from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
from django.core.cache import cache
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");
class MainView(TemplateView):
    template_name="front/main.html"
    def get(self,request,*args,**kwargs):
        # 获取openid，昵称，头像url,性别等信息
        # 按照openid,去查询profile,如果没有存在，就创建一个user,同时创建一个profile
        # 然后去模拟登录login
        if(request.user.is_authenticated is False):
            role=request.Get["role"];
            code=request.Get["code"];
            wxinfoUrl=settings.WX["WX_AUTH_URL_CODE"].replace("{code}",code);
            import httplib
            conn = httplib.HTTPConnection(wxinfoUrl)
            conn.request("GET", "/index.html")
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            data1 = r1.read()
            cache.set("ak",data1)
            decodeJson=json.loads(data1)
            print(decodeJson)
            conn.close()
            pass
        # 去微信认证
        # 认证通过后，需要创建用户，并login
        # 重新跳转到本页面
        return super(MainView,self).get(request,*args,**kwargs)
