from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from cms.models import WxWelcome
from back.models import JsonResultService
from django.conf import settings
import sys
import json
from django.core.cache import cache
import logging
logger = logging.getLogger("django")

# Create your views here.
class WxService(JsonResultService):
    def welcome(self,host):
        jsonResult=self.initJsonResult()
        content={}
        try:
            welcome= WxWelcome.objects.latest("createdTime")
            content=self.toJSON(welcome,["name","desc"])
            content["img"]=host+settings.MEDIA_URL+welcome.img.img.name
        except:
            info=sys.exc_info()
            logging.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult


wxService=WxService()
