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
from feedback.models import FeedBack,Post,Comment
import sys
import json
from django.core.cache import cache
import logging
import datetime
logger = logging.getLogger("django")

# Create your views here.
class FeedbackService(JsonResultService):
    def orghabits(self,org,role,schema,pid):
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
                # to do performance
                orgacthistorys=OrgActivityHistory.objects.filter(org__id__exact=org.id).filter(habits__contains=fstr).order_by("createdTime");
                for orgacthistory in orgacthistorys:
                    habitsArrayStr=orgacthistory.habits.split(",")
                    activity=orgacthistory.activity
                    for habitstr in habitsArrayStr:
                        habitstrArray=habitstr.split("|")
                        habittmp={}
                        habittmp["id"]=habitstrArray[0]
                        habittmp["name"]=habitstrArray[1]
                        habittmp["isForParent"]=habitstrArray[2]
                        habittmp["icon"]=habitstrArray[3]
                        habittmp["hid"]=orgacthistory.id

                        # 检查缓存是否已经反馈过uid:habitid:date
                        nowstr=datetime.datetime.now().strftime("%Y-%m-%d")
                        userid_habitid_date_key=settings.CACHE_FORMAT_STR['userid_habitid_date_key'] % (int(pid),int(habittmp["id"]),nowstr)

                        feedback=cache.get(userid_habitid_date_key)
                        if not feedback:
                            habittmp["isFeedBack"]="0"
                        else:
                            habittmp["isFeedBack"]="1"

                        # 取最近一次当前习惯的打卡
                        userid_habitid_key=settings.CACHE_FORMAT_STR['userid_habitid_key'] % (int(pid),int(habittmp["id"]),)
                        lastFeed=cache.get(userid_habitid_key)
                        if not lastFeed:
                            habittmp["accumDays"]=0
                            habittmp["freeMily"]=0
                            habittmp["accumMily"]=0
                        else:
                            habittmp["accumDays"]=lastFeed.accumDays
                            habittmp["freeMily"]=lastFeed.freeMily
                            habittmp["accumMily"]=lastFeed.accumMily
                        # habittmp["actImg"]=schema+settings.MEDIA_URL+activity.img.img.name
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

    def create(self,pid,habitid,hid,org):
        jsonResult=self.initJsonResult()
        content={}
        logger.error("create")
        userid_habitid_date_key=None
        userid_habitid_key=None
        lastFeed=None
        try:
            with transaction.atomic():
                # 创建反馈
                feedBack=FeedBack()
                # 查询出当前打卡用户,
                profileTmp=Profile.objects.get(pk=int(pid))
                feedBack.profile=profileTmp
                # 查询出当前活动历史,在创建活动历史的时候，建立缓存活动历史缓存,缓存时间是活动的时间
                acthistoryTmp=None
                # 活动历史缓存key
                acthistory_key=settings.CACHE_FORMAT_STR['acthistory_key'] % (int(hid))
                acthistoryTmp=cache.get(acthistory_key)
                if not acthistoryTmp:
                    acthistoryTmp=OrgActivityHistory.objects.get(pk=int(hid))
                    cache.set(acthistory_key,acthistoryTmp,acthistoryTmp.activityDays*24*3600)

                feedBack.orgActivityHistory=acthistoryTmp
                # 查询出当前打卡的习惯 to do 从缓存中取
                habitTmp=None
                habit_key=settings.CACHE_FORMAT_STR['habit_key'] % (int(habitid))
                habitTmp=cache.get(habit_key)
                if not habitTmp:
                    habitTmp=Habit.objects.get(pk=int(habitid))
                    cache.set(habit_key,habitTmp)
                feedBack.habit=habitTmp
                # 取最近一次当前习惯的打卡
                userid_habitid_key=settings.CACHE_FORMAT_STR['userid_habitid_key'] % (int(pid),int(habitid),)
                lastFeed=cache.get(userid_habitid_key)
                a1=feedBack.habit.freePraiseMilyUnit
                d=feedBack.habit.freePraiseMilyStep
                if lastFeed:
                    feedBack.accumDays=lastFeed.accumDays+1
                    feedBack.freeMily=a1+(feedBack.accumDays-1)*d
                    feedBack.accumMily=feedBack.accumDays*(a1+feedBack.freeMily)/2
                else:
                    # 获取当前用户最后一次的反馈
                    try:
                        lastFeed=FeedBack.objects.filter(profile__id=int(pid)).filter(habit__id=int(habitid)).order_by('-createdTime')[0]
                        cache.set(userid_habitid_key,lastFeed)
                        feedBack.accumDays=lastFeed.accumDays+1
                        feedBack.freeMily=a1+(feedBack.accumDays-1)*d
                        feedBack.accumMily=feedBack.accumDays*(a1+feedBack.freeMily)/2
                    except FeedBack.DoesNotExist:
                        feedBack.accumDays=1
                        feedBack.freeMily=a1
                        feedBack.accumMily=a1
                feedBack.save()
                #创建头贴*
                post=Post()
                post.feedBack=feedBack
                post.save()

                # 初始化缓存　Key:打卡用户id+habitid+打卡日期 feedBack:1-表示已经打卡，０表示未打卡
                userid_habitid_date_key=settings.CACHE_FORMAT_STR['userid_habitid_date_key'] % (int(pid),int(habitid),post.postDate)
                cache.set(userid_habitid_date_key,feedBack,settings.CACHE_FORMAT_STR['userid_habitid_date_key_timeout'])
                # 缓存最后一次打卡记录
                cache.set(userid_habitid_key,feedBack,acthistoryTmp.activityDays*24*3600)

                # 设置系统账户历史
                sysAccountHistory=SysAccountHistory()
                sysAccountHistory.tradeType=MAP_SYS_TRADE_TYPE["sysFreeOutMily"]
                sysAccountHistory.tradeAmount=-feedBack.freeMily

                # 设置系统账户
                sysAccount=cache.get("sysAccount")
                if not sysAccount:
                    sysAccount=SysAccount.objects.get(pk=settings.CACHE_FORMAT_STR['sys_mily_account_id'])

                sysAccountHistory.sysAccount=sysAccount
                sysAccountHistory.save()
                # 设置平台最新账户缓存
                cache.set("sysAccount",sysAccountHistory.sysAccount)
                # 设置个人账户历史　　　　　　　　　　
                accountHistory=AccountHistory()
                accountHistory.tradeType=MAP_TRADE_TYPE["feedBackMilyInput"]
                accountHistory.org=org
                accountHistory.operator=profileTmp
                accountHistory.activity=feedBack.orgActivityHistory.activity
                logger.error("accountHistory.activity=feedBack.orgActivityHistory.activity")
                accountHistory.sysAccountHistory=sysAccountHistory
                # 设置米仓账户
                accountkey=settings.CACHE_FORMAT_STR['account_mily_profileid_key'] % (int(pid))
                account=cache.get(accountkey)
                if not account:
                    logger.error("accountkey")
                    account=Account.objects.filter(profile__id=int(pid)).filter(accountType="rice")[0]
                accountHistory.account=account
                accountHistory.feedback=feedBack
                accountHistory.tradeAmount=feedBack.freeMily
                accountHistory.save()
                # 设置最新个人账户缓存
                cache.set(accountkey,accountHistory.account)
                # 返回当前帖子
                content["postid"]=post.id
        except Exception as e:
            logger.error(e)
            if userid_habitid_key:
                cache.set(userid_habitid_key,lastFeed)
            if userid_habitid_date_key:
                cache.delete(userid_habitid_date_key)
            # 清空当前保存的最后一个反馈和当前日期的反馈
            info=sys.exc_info()
            logging.error(info)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

feedbackService=FeedbackService()
