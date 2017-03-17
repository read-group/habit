from activity.models import Activity
from django.conf import settings
from feedback.models import OrgActivityHistory
from habitinfo.models import Habit
from back.models import JsonResultService
import sys
import json
from django.core.cache import cache
import logging
logger = logging.getLogger("django")
# Create your views here.
class ActivityService(JsonResultService):
    def activitys(self,skip,limit,schema):
        content={}
        data=[]
        try:
            queryCache=Activity.objects.order_by("createdTime");
            count=queryCache.count();
            acts= queryCache[skip:limit]
            for act in acts:
                dataTmp=self.toJSON(act,["id","name","code","startTime","endTime","zeroableMily","desc","isTop"])
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

    def activityDetail(self,id,schema):
        content={}
        try:
            act= Activity.objects.get(pk=id)
            dataTmp=self.toJSON(act,["id","name","code","startTime","endTime","desc",'memo','zeroableMily'])
            dataTmp["img"]=schema+settings.MEDIA_URL+act.img.img.name
            dataTmp["cat"]=act.get_cat_display()
            cats=[]
            for item in act.activityitem_set.all():
                habitCat=self.toJSON(item.cat,["id","name"])
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
            content["data"]=dataTmp
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
        try:
            # 获取家庭对象
            org=user.profile.org
            # 获取活动对象
            act= Activity.objects.get(pk=actid)
            logger.error(act.name)
            #获取匹配的习惯，从缓存中取，如果缓存不存在，就从数据库里去找
            habitArray=[]
            rtnArray=[]
            for cat in cats:
                catid=cat.id
                level2=cat.level
                habitLevelKeyRun=settings.CACHE_FORMAT_STR['cat_habit_level'] % (catid, level2)
                habitTmp=cache.get(habitLevelKeyRun)
                if not habitTmp:
                    # 去库里查询
                    habitTmp=Habit.objects.filter(habitCatalog__id=catid).filter(level=level2)
                dataTmp=self.toJSON(habitTmp,["id","name"])
                rtnArray.append(dataTmp)
                habitArray.append(habitTmp.id+"|"+habitTmp.name)
            habitStr=",".join(habitArray)
            # 构建参加活动历史.
            orgActivityHistory=OrgActivityHistory()
            orgActivityHistory.org=org
            orgActivityHistory.activity=act
            orgActivityHistory.habits=habitStr
            orgActivityHistory.save()
            # 构建家庭习惯缓存org:id:habit:id=habit
            orgActivityKey=settings.CACHE_FORMAT_STR['org_activity'] % (org.id)
            #计算缓存天数
            cacheDays=(act.endTime-act.startTime).days+1
            cache.set(orgActivityKey,orgActivityHistory,cacheDays)
            content["data"]=rtnArray
        except:
            info=sys.exc_info()
            logger.error(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult




activityService=ActivityService()
