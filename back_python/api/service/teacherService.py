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
class TeacherService(JsonResultService):
    def addclass(self,user,classinfo):
        jsonResult=self.initJsonResult()
        content={}
        try:
            logger.error("addclass")
            scodeClass=-1
            school=None
            try:
                scodeClass=int(classinfo["scode"])
                school=School.objects.get(pk=scodeClass)
            except:
                self.jsonResult.rtnDic["status"]=-1
                self.jsonResult.rtnDic["errMsg"]="请检查您输入的学校编码."
            nameClass=classinfo["name"]
            imgUrlClass=classinfo["imgUrl"]
            cg=ClassGroup(name=nameClass,imgUrl=imgUrlClass)
            cg.school=school
            cg.creator=user
            cg.save()
            content["cgid"]=cg.id
        except:
            info=sys.exc_info()
            logging.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult
    def classmember(self,user,cgid):
        jsonResult=self.initJsonResult()
        content={}
        cgArray=[]
        currentCgStudents=[]
        logger.error("TeacherService")
        try:
            cgs=ClassGroup.objects.filter(creator__id=user.id).order_by("createdTime");
            for cg in cgs:
                dataTmp=self.toJSON(cg,["id","name","imgUrl"])
                cgArray.append(dataTmp)
            cgidParam=int(cgid)
            profilesRtn=None
            if -1==cgidParam:
                cg=cgs[0]
                content["cgname"]=cg.name
                content["imgUrl"]=cg.imgUrl
                profilesRtn=cg.profile_set.all()
            else:
                cg=ClassGroup.objects.get(pk=cgidParam)
                content["cgname"]=cg.name
                content["imgUrl"]=cg.imgUrl
                profilesRtn=cg.profile_set.all()
            for p in profilesRtn:
                ptemp=self.toJSON(p,["id","nickname","imgUrl","childpwd",])
                accountkey=settings.CACHE_FORMAT_STR['account_mily_profileid_key'] % (p.id)
                account=cache.get(accountkey)
                if not account:
                    account=Account.objects.filter(profile__id=p.id).filter(accountType="rice")[0]
                    ptemp['milyAccount']=account.balance
                    cache.set(accountkey,account)
                else:
                    ptemp['milyAccount']=account.balance
                currentCgStudents.append(ptemp)
            content["cgArray"]=cgArray
            content["currentCgStudents"]=currentCgStudents

        except:
            info=sys.exc_info()
            logging.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

    def myfunc(self,user):
        jsonResult=self.initJsonResult()
        content={}
        try:
            logger.error(user.profile.nickname)
            dataTmp=self.toJSON(user.profile,["id","nickname","imgUrl",])
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

teacherService=TeacherService()
