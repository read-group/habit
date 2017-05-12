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
class GrainService(JsonResultService):
    def family(self,familyOrg,pf):
        jsonResult=self.initJsonResult()
        content={}
        data=[]
        logger.error("GrainService")
        try:
            profiles=Profile.objects.filter(org__id__exact=familyOrg.id).order_by("createdTime");
            for profile in profiles:
                dataTmp=self.toJSON(profile,["id","nickname","imgUrl","role","openid"])
                # 判断当前登录角色，如果是学生,那么需要判断当前登录用户的id与当前记录是否一致，一致则客户端可打卡，否则无法打卡
                dataTmp["canedit"]=1
                if pf.role=="4":
                    if dataTmp["id"]!=pf.id:
                        dataTmp["canedit"]=0
                accountkey=settings.CACHE_FORMAT_STR['account_mily_profileid_key'] % (profile.id)
                account=cache.get(accountkey)
                if not account:
                    account=Account.objects.filter(profile__id=profile.id).filter(accountType="rice")[0]
                    dataTmp['milyAccount']=account.balance
                    cache.set(accountkey,account)
                else:
                    dataTmp['milyAccount']=account.balance

                # 体力值
                # 体力值的缓存计算，body:profileid--key,value:val
                body_userid_key=settings.CACHE_FORMAT_STR['body_userid_key'] % (profile.id)
                bodyval=cache.get(body_userid_key)
                if bodyval:
                    dataTmp["bodyval"]=int(bodyval)
                else:
                    c=FeedBack.objects.filter(profile__id=profile.id).count()
                    cache.set("body_userid_key",c)
                    dataTmp["bodyval"]=c
                data.append(dataTmp)
            content["data"]=data
        except Exception as e:
            logger.error(e)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult


    def friends(self,pf):
        jsonResult=self.initJsonResult()
        content={}
        data=[]
        try:
            # 当前作为发起者的朋友
            for f in pf.fromFriendSet.select_related("top").all():
                profile=f.top
                dataTmp=self.toJSON(profile,["id","nickname","imgUrl","role","openid"])

                accountkey=settings.CACHE_FORMAT_STR['account_mily_profileid_key'] % (profile.id)
                account=cache.get(accountkey)
                if not account:
                    account=Account.objects.filter(profile__id=profile.id).filter(accountType="rice")[0]
                    dataTmp['milyAccount']=account.balance
                    cache.set(accountkey,account)
                else:
                    dataTmp['milyAccount']=account.balance
                data.append(dataTmp)

            # 当前用户作为接受者的朋友
            for f in pf.toFriendSet.select_related("fromp").all():
                profile=f.fromp
                dataTmp=self.toJSON(profile,["id","nickname","imgUrl","role","openid"])

                accountkey=settings.CACHE_FORMAT_STR['account_mily_profileid_key'] % (profile.id)
                account=cache.get(accountkey)
                if not account:
                    account=Account.objects.filter(profile__id=profile.id).filter(accountType="rice")[0]
                    dataTmp['milyAccount']=account.balance
                    cache.set(accountkey,account)
                else:
                    dataTmp['milyAccount']=account.balance
                data.append(dataTmp)
            content["data"]=data
        except:
            info=sys.exc_info()
            logging.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

    def addmember(self,familyOrg,childinfo):
        jsonResult=self.initJsonResult()
        logger.error("addmember ")
        content={}
        try:
            # 获取班级
            with transaction.atomic():
                # 创建新的用户信息
                userC=User.objects.create(username=childinfo["nickname"])
                # 查询班级
                classGroupF=None
                try:
                    #创建另一个Profile
                    profile=Profile(nickname=childinfo["nickname"],role=MapEngToRole["child"],
                    imgUrl=childinfo["headingImgUrl"],user=userC,org=familyOrg,childpwd=childinfo["password"])
                    profile.save()

                    #创建三个个人账户（米仓、现金、押金）
                    accountMily=Account()
                    accountMily.accountType="rice"
                    accountMily.profile=profile
                    accountMily.save()
                    accountCash=Account()
                    accountCash.accountType="cash"
                    accountCash.profile=profile
                    accountCash.save()

                    classGroups=[]
                    classids=childinfo["classid"].split(",")
                    if len(classids)==1:
                        try:
                            int(classids[0])
                        except:
                            classids=childinfo["classid"].split("，")
                        for cid in classids:
                            cg=ClassGroup.objects.get(pk=int(cid))
                            profile.classGroups.add(cg)
                    else:
                        cg=ClassGroup.objects.get(pk=7)
                        profile.classGroups.add(cg)
                except ClassGroup.DoesNotExist:
                    jsonResult.rtnDic["errMsg"]="请向管理员咨询您的班级号"
                # 获取班级
        except:
            logger.error("except............")
            info=sys.exc_info()
            logger.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

    def updatemember(self,childinfo):
        jsonResult=self.initJsonResult()
        logger.error("updatemember")
        content={}
        try:
            # 获取班级
            with transaction.atomic():
                # 用户信息
                try:
                    profile=Profile.objects.get(pk=int(childinfo["cid"]))
                    #创建另一个Profile
                    usertmp=profile.user
                    usertmp.username=childinfo["nickname"]
                    profile.nickname=childinfo["nickname"]
                    profile.imgUrl=childinfo["headingImgUrl"]
                    profile.childpwd=childinfo["password"]
                    # profile.role=MapEngToRole["child"]
                    # profile.org=familyOrg
                    usertmp.save()
                    profile.save()
                    profile.classGroups.clear()
                    classGroups=[]
                    classids=childinfo["classid"].split(",")
                    if len(classids)==1:
                        try:
                            int(classids[0])
                        except:
                            classids=childinfo["classid"].split("，")
                    for cid in classids:
                        cg=ClassGroup.objects.get(pk=int(cid))
                        profile.classGroups.add(cg)
                except User.DoesNotExist:
                    jsonResult.rtnDic["errMsg"]="请向管理员咨询您的班级号"
                # 获取班级
        except:
            info=sys.exc_info()
            logger.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

    def getmember(self,cid):
        jsonResult=self.initJsonResult()
        logger.error("getmember ")
        content={}
        try:
            # 创建新的用户信息
            profile=Profile.objects.get(pk=cid)
            content=self.toJSON(profile,["id","nickname","imgUrl","childpwd",])
            cgids=[]
            for cg in profile.classGroups.all():
                cgids.append(str(cg.id))
            cgidstr=",".join(cgids)
            content["classids"]=cgidstr
        except:
            info=sys.exc_info()
            logger.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult


grainService=GrainService()
