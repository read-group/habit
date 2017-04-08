from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from org.models import Profile,MapEngToRole,Org
from school.models import ClassGroup
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
class FeedbackService(JsonResultService):
    def orghabits(self,org,role):
        jsonResult=self.initJsonResult()
        content={}
        data=[]
        logger.error("FeedbackService")
        try:
            with transaction.atomic():
                fstr=None
                if role=="4":
                    fstr="p0"
                else:
                    fstr="p1"
                orgacthistorys=OrgActivityHistory.objects.filter(org__id__exact=org.id).filter(habits__contains=fstr).order_by("createdTime");
                for orgacthistory in orgacthistorys:
                    habitsArrayStr=orgacthistory.habits.split(",")
                    for habitstr in habitsArrayStr:
                        habitstrArray=habitstr.split("|")
                        habittmp={}
                        habittmp["id"]=habitstrArray[0]
                        habittmp["name"]=habitstrArray[1]
                        habittmp["isForParent"]=habitstrArray[2]
                        habittmp["icon"]=habitstrArray[3]
                        habittmp["isFeedBack"]="1"
                        if fstr==habittmp["isForParent"]:
                            data.append(habittmp)
                content["data"]=data
        except:
            info=sys.exc_info()
            logging.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

feedbackService=FeedbackService()
