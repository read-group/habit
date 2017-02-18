from django.shortcuts import render
from cms.models import WxWelcome
from django.conf import settings
from back.models import JsonResultView
import sys
import json
# Create your views here.
class WxWelcomeView(JsonResultView):
    def get(self,req,*arg,**kwargs):
        data=None
        try:
            welcome= WxWelcome.objects.latest("createdTime")
            # data["name"]=welcome.name
            # data["desc"]=welcome.desc
            # data["img"]=welcome.img.img.name
            data=self.toJSON(welcome,["name","desc"])
            data["img"]=req.scheme+"://"+req.META["HTTP_HOST"]+settings.MEDIA_URL+welcome.img.img.name
            print(data["img"])
        except:
            info=sys.exc_info()
            print(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=data
        finally:
            return self.jsonResult.renderToJsonResponse()
    def post(self,req,*arg,**kwargs):
        data=json.loads(request.raw_post_data)
    def getQuerySet(self):
        return
