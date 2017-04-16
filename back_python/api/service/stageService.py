from django.db import transaction
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.models import User
from org.models import Profile,MapEngToRole,Org,Friend
from school.models import ClassGroup
import datetime
from activity.models import Activity
from django.conf import settings
from feedback.models import OrgActivityHistory
from account.models import Account,AccountHistory,SysAccountHistory,SysAccount,MAP_TRADE_TYPE,MAP_ACCOUNT_TYPE,MAP_SYS_TRADE_TYPE
from habitinfo.models import Habit
from back.models import JsonResultService
from feedback.models import FeedBack,Post,Comment,Map_Comment_TYPE
import sys
import json
from django.core.cache import cache
import logging
import datetime
logger = logging.getLogger("django")

# Create your views here.
class StageService(JsonResultService):
    def postlist(self,skip,limit,pid):
        jsonResult=self.initJsonResult()
        content={}
        data=[]
        try:
            queryCache=None
            if int(pid)==-1:
                queryCache=Post.objects.select_related('feedBack').order_by("createdTime");
            else:
                queryCache=Post.objects.select_related('feedBack').filter(feedBack__profile__id=int(pid)).order_by("createdTime");

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

    def prase(self,postid,profile):
        jsonResult=self.initJsonResult()
        content={}
        data=[]
        praseInfos=[]
        audioInfos=[]
        try:
            with transaction.atomic():
                postQuery=Post.objects.select_related("feedBack").filter(id=int(postid));
                post=postQuery[0]
                # 按照当前点评者、按照postid查询是否已经点评过,如果点评过，就
                comment=Comment()
                comment.commentType=Map_Comment_TYPE["prase"]
                comment.post=post
                comment.fromProfile=profile
                comment.save()
                # 加好友
                # postCreator=post.feedBack.profile
                # if postCreator.id==profile.id:
                #     pass
                # else:
                #     friends=Friend()
                #     friends.from_profile=profile
                #     friends.to_profile=postCreator
                #     friends.save()
                # 增加帖子上的赞扬次数
                postQuery.update(accumPrases=F("accumPrases")+1)


                # 发送赞扬通知，给被赞扬者

                #返回这个帖子，包括了


            content["data"]=data
        except Exception as e:
            logger.error(e)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult
stageService=StageService()
