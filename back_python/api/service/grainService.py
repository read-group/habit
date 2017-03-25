from django.db import transaction
from django.db.models import Q
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
    def addmember(self,familyOrg,childinfo):
        logger.error("addmember ")
        content={}
        try:
            with transaction.atomic():
                # 创建新的用户信息
                userC=User.objects.create(username=childinfo["nickname"])
                # 查询班级
                classGroupF=None
                try:

                    classGroupF=ClassGroup.objects.get(pk=int(childinfo["classid"]))
                except ClassGroup.DoesNotExist:
                    self.jsonResult.rtnDic["errMsg"]="请向管理员咨询您的班级号"
                #创建另一个Profile
                profile=Profile(nickname=childinfo["nickname"],role=MapEngToRole["child"],
                imgUrl=childinfo["headingImgUrl"],user=userC,org=familyOrg,classGroup=classGroupF)
                profile.save()
        except:
            info=sys.exc_info()
            logger.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult


grainService=GrainService()
