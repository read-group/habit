from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
from django.core.cache import cache
import logging
logger = logging.getLogger("django")
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");
class MainView(TemplateView):
    template_name="front/main.html"
    def get(self,request,*args,**kwargs):
        # 获取openid，昵称，头像url,性别等信息
        # 按照openid,去查询profile,如果没有存在，就创建一个user,同时创建一个profile
        # 然后去模拟登录login
        logger.debug("begin main")
        logger.debug(request.user.is_authenticated)
        if(not request.user.is_authenticated):
            logger.debug("begin fetch token....")
            role=request.GET["role"];
            code=request.GET["code"];
            wxinfoUrl=settings.WX["WX_AUTH_URL_INFO"].replace("{code}",code);
            logger.debug(wxinfoUrl)
            import urllib.request
            response = urllib.request.urlopen(wxinfoUrl)
            r1 = response.read()
            logger.debug("data1================")
            logger.debug(r1)
            decodeJson=json.loads(r1)
            logger.debug(decodeJson["access_token"])
            logger.debug(decodeJson["openid"])
            # 按照访问token再去获取用户信息
            userInfoUrl=settings.WX["WX_AUTH_USER_INFO"] % (decodeJson["access_token"],decodeJson["openid"])

            response=urllib.request.urlopen(userInfoUrl)
            r2 = response.read()
            logger.debug(r2)
            decodeUserInfoJson=json.loads(r2)
            pass
        # 去微信认证
        # 认证通过后，需要创建用户，并login
        # 重新跳转到本页面
        return super(MainView,self).get(request,*args,**kwargs)
