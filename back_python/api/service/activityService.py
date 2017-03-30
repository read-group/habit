from django.db import transaction
from django.db.models import Q
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
class ActivityService(JsonResultService):
    # 参与懒人基金分享
    def lazyFundShareIn(self,user,actId):
        content={}
        data={}
        try:
            # 需要建立事务
            # 按照活动id,按照用户id,去查询活动历史，修改启用懒人基金标志，活动历史id作为业务单据id

            # 调用微信服务，生成一个虚拟订单,把活动历史id传进去，返回支付参数给客户端,返回历史订单id,如果失败，设置活动历史参与状态为０
            content["data"]=data
        except (Exception ,e):
            info=sys.exc_info()
            logging.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult

    def activitys(self,skip,limit,schema,tag):
        content={}
        data=[]
        try:
            topQuery=(tag=='t')
            queryCache=Activity.objects.filter(isTop__exact=topQuery).filter(status__exact=1).order_by("createdTime");
            count=queryCache.count();

            acts= queryCache[skip:limit]
            for act in acts:
                dataTmp=self.toJSON(act,["id","name","code","startTime","endTime","desc","isTop",'applyNumber','uplimit','days','cat','amount',])
                dataTmp["img"]=schema+settings.MEDIA_URL+act.img.img.name
                dataTmp["cat"]=act.get_cat_display()
                data.append(dataTmp)
            content["total"]=count
            content["data"]=data
        except (Exception ,e):
            info=sys.exc_info()
            logging.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult

    def activityDetail(self,user,id,schema):
        content={}
        try:
            act= Activity.objects.get(pk=id)

            # 检查活动状态，如果当前查看的时间大于活动开始时间而小于活动结束时间
            dataTmp=self.toJSON(act,["id","name","code","startTime","endTime","desc",'memo','status','applyNumber','uplimit','days','rtnLazyUnit','amount','cat',])

            dataTmp["img"]=schema+settings.MEDIA_URL+act.img.img.name
            dataTmp["cat"]=act.get_cat_display()
            cats=[]

            for item in act.activityitem_set.all():
                habitCat=self.toJSON(item.cat,["id","name","forParent"])

                #设置习惯类别的级别初值
                habitCat["level"]="M"
                #在查询出当前活动时，应该把当前活动的习惯类别所涉及的习惯加载到缓存，缓存key是：cat:id:habit:level,值是习惯
                for habit in item.cat.habit_set.all():
                    habitLevelKey=settings.CACHE_FORMAT_STR['cat_habit_level'] % (item.cat.id, habit.level)
                    habitLevelCache=cache.get(habitLevelKey)
                    if not habitLevelCache:
                        cache.set(habitLevelKey,habit,settings.CACHE_FORMAT_STR['cat_habit_level_timeout'])

                cats.append(habitCat)
            dataTmp["habitCat"]=cats
            # 检查是否已经报名
            org=user.profile.org
            orgActivityKey=settings.CACHE_FORMAT_STR['org_activity'] % (org.id)
            orgActivityHistorys=cache.get(orgActivityKey)
            dataTmp["applied"]="0"
            dataTmp["lazyIn"]=act.lazyJoinNumber
            if not orgActivityHistorys:
                # 先去库里获取
                orgActivityHistorys=list(OrgActivityHistory.objects.filter(org__id=org.id))

            for oac in orgActivityHistorys:
                if oac.activity.id==dataTmp["id"]:
                    dataTmp["applied"]="1"
                    break;

            content["data"]=dataTmp
        except:
            info=sys.exc_info()
            logger.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult


    def activityLoopCheck(self):
        content={}
        try:
            dnow=datetime.datetime.now()
            # 查询出未开始和进行中的活动
            activitysRunning=Activity.objects.filter(Q(startTime__lt=dnow) & Q(endTime__gt=dnow))
            activitysRunning.update(status=1)
            activitysEnding=Activity.objects.filter(Q(endTime__lte=dnow))
            activitysEnding.update(status=-1)
        except:
            info=sys.exc_info()
            logger.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult


    def activityJoin(self,user,actid,cats):
        content={}
        lazyInfo={}
        try:
            # 获取家庭对象
            org=user.profile.org
            # 获取活动对象
            activity= Activity.objects.get(pk=actid)
            #检查活动状态，如果当前时间大于开始时间
            #获取匹配的习惯，从缓存中取，如果缓存不存在，就从数据库里去找
            habitArray=[]
            rtnArray=[]
            for cat in cats:
                catid=cat["id"]
                level2=cat["level"]
                isForParent='p0'
                if cat["forParent"]:
                    isForParent='p1'
                else:
                    isForParent='p0'
                # 判断习惯类别是否需要诊断，是否是父母习惯，如果是不需要诊断,level默认是M,
                # 如果是不需要诊断,level2＝‘M/L’

                habitLevelKeyRun=settings.CACHE_FORMAT_STR['cat_habit_level'] % (catid, level2)
                habitTmp=cache.get(habitLevelKeyRun)
                if not habitTmp:
                    # 去库里查询
                    habitTmp=Habit.objects.filter(habitCatalog__id=catid).filter(level=level2)
                    cache.set(habitLevelKeyRun,habitTmp,settings.CACHE_FORMAT_STR['cat_habit_level_timeout'])

                dataTmp=self.toJSON(habitTmp,["id","name","icon"])
                rtnArray.append(dataTmp)
                # 如果是父母习惯，加一个字段区分,0专用，-1非专用
                habitArray.append(str(habitTmp.id)+"|"+habitTmp.name+"|"+isForParent+"|"+habitTmp.icon)
            habitStr=",".join(habitArray)
            with transaction.atomic():
                # 构建参加活动历史.
                orgActivityHistory=OrgActivityHistory()
                orgActivityHistory.org=org
                orgActivityHistory.activity=activity
                if activity.cat=="FREE":
                    orgActivityHistory.isFree=True
                else:
                    orgActivityHistory.isFree=False
                # 活动赠米
                # orgActivityHistory.getMily=activity.zeroableMily
                orgActivityHistory.habits=habitStr
                # 活动持续天数
                orgActivityHistory.activityDays=activity.days
                # 懒人基金金额
                orgActivityHistory.lazyFund=activity.lazyFund

                orgActivityHistory.save()

                # 更新活动报名人数
                activity.applyNumber=activity.applyNumber+1
                if activity.applyNumber>activity.uplimit:
                    self.jsonResult.rtnDic['errMsg']="名额已满，请下期再报！"
                    raise Exception("名额已满，请下期再报！")
                else:
                    activity.save()


                # # 平台米仓修改
                # sysAccountHistory=SysAccountHistory()
                # sysAccountHistory.tradeType=MAP_SYS_TRADE_TYPE["sysFreeOutMily"]
                # sysAccountHistory.tradeAmount=0-orgActivityHistory.getMily
                # # 查询米仓类型的系统账户
                # sysAccount=SysAccount.objects.get(accountType__exact=MAP_ACCOUNT_TYPE["rice"])
                # sysAccountHistory.sysAccount=sysAccount
                # sysAccountHistory.save()
            # 构建家庭习惯缓存org:id:habit:id=habit
            orgActivityKey=settings.CACHE_FORMAT_STR['org_activity'] % (org.id)
            #计算缓存天数
            cacheDays=(activity.endTime-activity.startTime).days+1

            org_activitys=cache.get(orgActivityKey)
            if not org_activitys:
                # 先去库里获取
                org_activitys=list(OrgActivityHistory.objects.filter(org__id=org.id))
                if not org_activitys:
                    org_activitys=[orgActivityHistory]
            else:
                org_activitys.push(orgActivityHistory)
            cache.set(orgActivityKey,org_activitys,cacheDays)
            content["data"]=rtnArray


            #
        except:
            info=sys.exc_info()
            logger.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult

activityService=ActivityService()
