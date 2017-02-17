from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from cms.models import WxWelcome
import json
class JsonResult(object):
    def __init__(self,status=0,content=None,rawErr=None,errMsg=None,
    help="status-0 indicate sucess,or 1 indicate fail"):
        self.rtnDic={}
        rtnDic.status=0
        rtnDic.content=content
        rtnDic.rawErr=rawErr
        rtnDic.errMsg=errMsg
        rtnDic.help="status-0 indicate sucess,or 1 indicate fail"
        super(JsonResult,self).__init__(self.rtnDic)
    def renderToJsonResponse(self):
        return JsonResponse(self.rtnDic)

# Create your views here.
class WxWelcome(View):
    def get(req,*arg,**kwargs):
        jsonResult=JsonResult()
        try:
            welcome=WxWelcome.objects.latest('createdTime')
        except:
            jsonResult.rtnDic.status=-1
        else:
            jsonResult.rtnDic.content=welcome.toJSON()
        finally:
            return jsonResult.renderToJsonResponse()
    def post(req,*arg,**kwargs):
        data=json.loads(request.raw_post_data)
        print(type(data))
