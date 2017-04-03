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
        cgArray=[]
        currentCgStudents=[]
        logger.error("TeacherService")
        try:
            logger.error(user.username)
            cgs=ClassGroup.objects.filter(creator__id=user.id).order_by("createdTime");
            logger.error("vvvvvvvvvv")
            logger.error(cgid)
            for cg in cgs:
                dataTmp=self.toJSON(cg,["id","name"])
                cgArray.append(dataTmp)
            cgidParam=int(cgid)
            profilesRtn=None
            if -1==cgidParam:
                logger.error("-1============")
                profilesRtn=cgs[0:1].profile_set
                logger.error(len(profilesRtn))
                logger.error("-1============")
            else:
                logger.error("no -1============")
                cg=ClassGroup.objects.get(pk=cgidParam)
                logger.error("after cg ============")
                profilesRtn=cg.profile_set
                logger.error("after profilesRtn ============")
            for p in profilesRtn:
                ptemp=self.toJSON(p,["id","nickname","imgUrl","childpwd",])
                currentCgStudents.append(ptemp)
            content["cgArray"]=cgArray
            content["currentCgStudents"]=currentCgStudents
        except:
            logging.error("error...............")
            info=sys.exc_info()
            logging.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult


teacherService=TeacherService()
