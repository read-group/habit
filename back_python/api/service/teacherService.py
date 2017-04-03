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
class TeacherService(JsonResultService):
    def classmember(self,user,cgid):
        content={}
        data=[]
        logger.error("TeacherService")
        try:
            logger.error(user.username)
            cgs=ClassGroup.objects.filter(creator__id=user.id);
            logger.error("vvvvvvvvvv")
            logger.error(cgid)
            for cg in cgs:
                dataTmp=self.toJSON(cg,["id","name"])
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


teacherService=TeacherService()
