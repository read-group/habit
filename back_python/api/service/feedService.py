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
import random
logger = logging.getLogger("django")
# http://mily365.com/media/upload/幻灯片3.PNG
randPic=['http://mily365.com/static/front/img/loop1.jpg','http://mily365.com/static/front/img/loop2.jpg','http://mily365.com/static/front/img/loo3.jpg','http://mily365.com/static/front/img/loop4.jpg']
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
                orgacthistorys=OrgActivityHistory.objects.filter(org__id__exact=org.id).filter(activity__status__exact=1).filter(habits__contains=fstr).order_by("createdTime");
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
                        habittmp["aid"]=activity.id
                        # 检查缓存是否已经反馈过uid:habitid:date
                        nowstr=datetime.datetime.now().strftime("%Y-%m-%d")
                        userid_habitid_date_key=settings.CACHE_FORMAT_STR['actid_userid_habitid_date_key'] % (activity.id,int(pid),int(habittmp["id"]),nowstr)

                        feedback=cache.get(userid_habitid_date_key)
                        if not feedback:
                            habittmp["isFeedBack"]="0"
                            habittmp["postid"]=-1
                        else:
                            habittmp["isFeedBack"]="1"
                            habittmp["postid"]=feedback.post.id

                        # 取最近一次当前习惯的打卡
                        userid_habitid_key=settings.CACHE_FORMAT_STR['actid_userid_habitid_key'] % (activity.id,int(pid),int(habittmp["id"]),)
                        lastFeed=cache.get(userid_habitid_key)
                        if not lastFeed:
                            try:
                                lastFeed=FeedBack.objects.filter(profile__id=int(pid)).filter(orgActivityHistory__id=orgacthistory.id).filter(habit__id=int(habittmp["id"])).order_by('-createdTime')[0]
                                habittmp["accumDays"]=lastFeed.accumDays
                                habittmp["freeMily"]=lastFeed.freeMily
                                habittmp["accumMily"]=lastFeed.accumMily
                                cache.set(userid_habitid_key,lastFeed)
                            except:
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

    def publish(self,pinfo):
        jsonResult=self.initJsonResult()
        content={}
        logger.error("publish")
        try:
            with transaction.atomic():
                # to do performance
                post=Post.objects.get(pk=int(pinfo['postid']))
                post.content=pinfo['content']
                if pinfo['imageUrl']=="#":
                    rp=random.choice(randPic)
                    post.imgUrl=rp
                else:
                    post.imgUrl=pinfo['imageUrl']
                post.audioUrls=pinfo['audioUrls']
                post.feel=pinfo['feel']
                post.save()
        except:
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult


    def milyOrder(self):
        jsonResult=self.initJsonResult()
        content={}
        data=[]
        logger.error("milyOrder")
        try:
            with transaction.atomic():
                # to do performance
                accounts=Account.objects.select_related("profile").filter(accountType="rice").order_by('-balance')[0:10]
                for a in accounts:
                    p=a.profile;
                    dataTmp=self.toJSON(p,["id","nickname","imgUrl","role","openid"])
                    dataTmp["mily"]=a.balance
                    data.append(dataTmp)
            content["data"]=data
        except:
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

    def cancel(self,postid):
        jsonResult=self.initJsonResult()
        content={}
        logger.error("cancel")
        try:
            with transaction.atomic():
                post=Post.objects.select_related("feedBack").get(pk=int(postid))
                feedback=post.feedBack
                logger.error("feedback")
                orgActivityHistory=feedback.orgActivityHistory
                profile=feedback.profile
                activity=orgActivityHistory.activity
                actid=activity.id
                pid=profile.id
                habitid=feedback.habit.id

                # 取最近一次当前习惯的打卡Key
                userid_habitid_key=settings.CACHE_FORMAT_STR['actid_userid_habitid_key'] % (actid,pid,habitid,)
                userid_habitid_date_key=settings.CACHE_FORMAT_STR['actid_userid_habitid_date_key'] % (actid,pid,habitid,post.postDate)
                userid_date_key=settings.CACHE_FORMAT_STR['userid_date_key'] % (pid,post.postDate)
                # 减少体力值
                body_userid_key=settings.CACHE_FORMAT_STR['body_userid_key'] % (pid)


                # 设置系统账户历史
                sysAccountHistory=SysAccountHistory()
                sysAccountHistory.tradeType=MAP_SYS_TRADE_TYPE["sysFreeOutMilyCancel"]
                sysAccountHistory.tradeAmount=feedback.freeMily

                # 设置系统账户feedback
                sysAccount=cache.get("sysAccount")
                if not sysAccount:
                    sysAccount=SysAccount.objects.get(pk=settings.CACHE_FORMAT_STR['sys_mily_account_id'])
                sysAccountHistory.sysAccount=sysAccount
                sysAccountHistory.save()
                # 设置平台最新账户缓存
                cache.set("sysAccount",sysAccountHistory.sysAccount)

                # 设置个人账户历史　　　　　　　　　　
                accountHistory=AccountHistory()
                accountHistory.tradeType=MAP_TRADE_TYPE["feedBackMilyInputCancel"]
                accountHistory.org=orgActivityHistory.org
                accountHistory.operator=profile
                accountHistory.activity=activity
                logger.error("accountHistory.activity=feedBack.orgActivityHistory.activity")
                accountHistory.sysAccountHistory=sysAccountHistory
                # 设置米仓账户
                accountkey=settings.CACHE_FORMAT_STR['account_mily_profileid_key'] % (pid)
                account=cache.get(accountkey)
                if not account:
                    logger.error("accountkey")
                    account=Account.objects.filter(profile__id=pid).filter(accountType="rice")[0]
                accountHistory.account=account
                accountHistory.feedback=feedback
                accountHistory.tradeAmount=-feedback.freeMily
                accountHistory.save()
                # 设置最新个人账户缓存
                cache.set(accountkey,accountHistory.account)

                feedback.delete()
                #清空最近一次的缓存
                cache.delete(userid_habitid_key)
                cache.delete(userid_habitid_date_key)
                cache.delete(userid_date_key)
                # 减少一个体力值
                cache.decr(body_userid_key)
                # 返回当前帖子对应的习惯
                content["habitid"]=int(habitid)

        except Exception as e:
            logger.error(e)
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
        userid_date_key=None
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
                # 设置当前活动
                act=feedBack.orgActivityHistory.activity

                # 查询出当前打卡的习惯 to do 从缓存中取
                habitTmp=None
                habit_key=settings.CACHE_FORMAT_STR['habit_key'] % (int(habitid))
                habitTmp=cache.get(habit_key)
                if not habitTmp:
                    habitTmp=Habit.objects.get(pk=int(habitid))
                    cache.set(habit_key,habitTmp)
                feedBack.habit=habitTmp
                # 取最近一次当前习惯的打卡
                userid_habitid_key=settings.CACHE_FORMAT_STR['actid_userid_habitid_key'] % (act.id,int(pid),int(habitid),)
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
                        lastFeed=FeedBack.objects.filter(profile__id=int(pid)).filter(orgActivityHistory__id=int(hid)).filter(habit__id=int(habitid)).order_by('-createdTime')[0]
                        cache.set(userid_habitid_key,lastFeed)
                        feedBack.accumDays=lastFeed.accumDays+1
                        feedBack.freeMily=a1+(feedBack.accumDays-1)*d
                        feedBack.accumMily=feedBack.accumDays*(a1+feedBack.freeMily)/2
                    except:
                        feedBack.accumDays=1
                        feedBack.freeMily=a1
                        feedBack.accumMily=a1

                # 体力值的缓存计算，body:profileid--key,value:val
                body_userid_key=settings.CACHE_FORMAT_STR['body_userid_key'] % (int(pid))
                bodyval=cache.get(body_userid_key)
                if not bodyval:
                    c=FeedBack.objects.filter(profile__id=int(pid)).count()
                    if c==0:
                        cache.set(body_userid_key,1,None)
                    else:
                        cc=c+1
                        cache.set(body_userid_key,cc,None)

                    # 更新统计值
                else:
                    cache.incr(body_userid_key)
                try:
                    feedBack.save()
                except:
                    cache.decr(body_userid_key)
                #创建头贴*
                post=Post()
                post.feedBack=feedBack
                rp=random.choice(randPic)
                post.imgUrl=rp
                post.content="这家伙一句留言都没有...."
                post.save()

                # 初始化缓存　Key:打卡用户id+habitid+打卡日期 feedBack:1-表示已经打卡，０表示未打卡
                userid_habitid_date_key=settings.CACHE_FORMAT_STR['actid_userid_habitid_date_key'] % (act.id,int(pid),int(habitid),post.postDate)
                cache.set(userid_habitid_date_key,feedBack,settings.CACHE_FORMAT_STR['userid_habitid_date_key_timeout'])
                # 记录用户当前日期是否打卡
                userid_date_key=settings.CACHE_FORMAT_STR['userid_date_key'] % (int(pid),post.postDate)
                cache.set(userid_date_key,1,settings.CACHE_FORMAT_STR['userid_date_key_timeout'])

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
                cache.set("sysAccount",sysAccountHistory.sysAccount,None)
                # 设置个人账户历史　　　　　　　　　　
                accountHistory=AccountHistory()
                accountHistory.tradeType=MAP_TRADE_TYPE["feedBackMilyInput"]
                accountHistory.org=org
                accountHistory.operator=profileTmp
                accountHistory.activity=act
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
                cache.set(accountkey,accountHistory.account,None)
                # 返回当前帖子
                content["postid"]=post.id
                content["habitid"]=int(habitid)
        except Exception as e:
            logger.error(e)
            if userid_habitid_key:
                # cache.set(userid_habitid_key,lastFeed)
                cache.delete(userid_habitid_key)
            if userid_habitid_date_key:
                cache.delete(userid_habitid_date_key)
            if userid_date_key:
                cache.delete(userid_date_key)
            # 清空当前保存的最后一个反馈和当前日期的反馈
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

    def getShareFeedInfo(self,aid,pid,hid):
        jsonResult=self.initJsonResult()
        content={}
        logger.error("getShareFeedInfo")
        try:
            habit=Habit.objects.get(pk=int(hid))
            profile=Profile.objects.get(pk=int(pid))
            userid_habitid_key=settings.CACHE_FORMAT_STR['actid_userid_habitid_key'] % (int(aid),int(pid),int(hid),)
            lastFeed=cache.get(userid_habitid_key)
            content["nickName"]=profile.nickname
            content["headingImgUrl"]=profile.imgUrl
            content["habitname"]=habit.name
            content["accumDays"]=lastFeed.accumDays
            content["freeMily"]=lastFeed.freeMily
            content["accumMily"]=lastFeed.accumMily
        except Exception as e:
            logger.error(e)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

feedbackService=FeedbackService()
