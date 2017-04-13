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
class StageService(JsonResultService):
    def postlist(self,skip,limit):

        jsonResult=self.initJsonResult()
        content={}
        data=[]
        try:
            queryCache=Post.objects.select_related('feedBack').order_by("createdTime");
            count=queryCache.count();
            posts= queryCache[skip:limit]
            for post in posts:
                dataTmp=self.toJSON(post,["id","content","imgUrl","audioUrls","postDate"])
                dataTmp["nickname"]=post.feedBack.profile.nickname
                dataTmp["headingImgUrl"]=post.feedBack.profile.imgUrl
                dataTmp["accumDays"]=post.feedBack.accumDays
                dataTmp["habitName"]=post.feedBack.habit.name
                logger.error(dataTmp)
                data.append(dataTmp)
            content["total"]=count
            content["data"]=data
        except Exception as e:
            logger.error(e)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult

stageService=StageService()
