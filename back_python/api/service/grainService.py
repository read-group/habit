from django.db import transaction
from django.db.models import Q
from org.models import Profile
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
class GrainService(JsonResultService):
    def family(self,familyOrg):
        content={}
        data=[]
        logger.error("GrainService")
        try:
            profiles=Profile.objects.filter(org__id__exact=familyOrg.id).order_by("createdTime");
            for profile in profiles:
                dataTmp=self.toJSON(profile,["id","nickname","imgUrl","role","openid"])
                data.append(dataTmp)
            content["data"]=data
        except:
            info=sys.exc_info()
            logging.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult

grainService=GrainService()
