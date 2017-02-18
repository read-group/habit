from django.shortcuts import render
from back.models import JsonResultView
from cms.models import WxWelcome

import sys
import json
# Create your views here.
class WxWelcomeView(JsonResultView):
    def get(self,req,*arg,**kwargs):
        try:
            d=self.getJsonedDataSet()
        except:
            info=sys.exc_info()
            print(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=d
        finally:
            return self.jsonResult.renderToJsonResponse()
    def post(self,req,*arg,**kwargs):
        data=json.loads(request.raw_post_data)

    def getQuerySet(self):
        return WxWelcome.objects.latest("createdTime")
