from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from org.models import Profile,MapEngToRole,Org
from school.models import ClassGroup,School
import datetime
from activity.models import Activity
from django.conf import settings
from feedback.models import OrgActivityHistory
from account.models import Account,AccountHistory,SysAccountHistory,SysAccount,MAP_TRADE_TYPE,MAP_ACCOUNT_TYPE,MAP_SYS_TRADE_TYPE
from habitinfo.models import Habit
from back.models import JsonResultService
import sys
import json
from django.core.cache import cache
import logging
logger = logging.getLogger("django")

# Create your views here.
class HomeService(JsonResultService):
    def myfunc(self,user):
        jsonResult=self.initJsonResult()
        content={}
        try:
            dataTmp=self.toJSON(user.profile,["id","nickname","imgUrl","role"])
            logger.error(dataTmp['nickname'])
            content["myinfo"]=dataTmp
        except:
            info=sys.exc_info()
            logging.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

homeService=HomeService()
