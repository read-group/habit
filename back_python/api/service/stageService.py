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
    def postlist(self,skip,limit,pid,currentUser):
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
                dataTmp=self.toJSON(post,["id","content","imgUrl","audioUrls","postDate","accumPrases","accumContents",])
                dataTmp["nickname"]=post.feedBack.profile.nickname
                dataTmp["headingImgUrl"]=post.feedBack.profile.imgUrl
                dataTmp["accumDays"]=post.feedBack.accumDays
                dataTmp["habitName"]=post.feedBack.habit.name
                # 构造post字典
                self._makeComments(post,dataTmp,currentUser)
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

    def _makeComments(self,post,postDic,currentUser):
        praseInfos=[]
        audioInfos=[]
        txtInfos=[]
        moneyInfos=[]
        # 默认当前帖子当前用户没有点赞
        postDic["isPrased"]=0
        for comment in post.comment_set.all():
            if comment.commentType=="prase":
                praseinfoTmp={}
                praseinfoTmp['imgUrl']=comment.fromProfile.imgUrl
                praseInfos.append(praseinfoTmp)
                if currentUser.id==comment.fromProfile.id:
                    postDic["isPrased"]=1
                    postDic["accumPrases"]=post.accumPrases

            if comment.commentType=="txt":
                txtinfoTmp={}
                txtinfoTmp['imgUrl']=comment.fromProfile.imgUrl
                txtinfoTmp['content']=comment.content
                txtInfos.append(txtinfoTmp)
            if comment.commentType=="sound":
                soundinfoTmp={}
                soundinfoTmp['imgUrl']=comment.fromProfile.imgUrl
                soundinfoTmp['audioUrls']=comment.audioUrls
                audioInfos.append(soundinfoTmp)
            if comment.commentType=="money":
                moneyinfoTmp={}
                moneyinfoTmp['imgUrl']=comment.fromProfile.imgUrl
                moneyInfos.append(moneyinfoTmp)

        postDic["praseInfos"]=praseInfos
        postDic["txtInfos"]=txtInfos
        postDic["audioInfos"]=audioInfos
        postDic["moneyInfos"]=moneyInfos
        return postDic

    def comment(self,postid,profile,commentType):
        jsonResult=self.initJsonResult()
        content={}
        data=[]
        postDic={}
        try:
            logger.error("comment..........")
            with transaction.atomic():
                postQuery=Post.objects.select_related("feedBack").filter(id=int(postid));
                post=postQuery[0]

                # postDic=self.toJSON(post,["id","content","imgUrl","audioUrls","postDate","accumPrases","accumContents",])
                # postDic["nickname"]=post.feedBack.profile.nickname
                # postDic["headingImgUrl"]=post.feedBack.profile.imgUrl
                # postDic["accumDays"]=post.feedBack.accumDays
                # postDic["habitName"]=post.feedBack.habit.name
                # 按照当前点评者、按照postid查询是否已经点评过,如果点评过，就
                comment=Comment()
                comment.commentType=commentType
                comment.post=post
                comment.fromProfile=profile
                comment.save()
                # 加好友
                postCreator=post.feedBack.profile
                if postCreator.id!=profile.id:
                    friends=Friend()
                    friends.from_profile=profile
                    friends.to_profile=postCreator
                    friends.save()
                # 增加帖子上的赞扬次数
                if commentType=="prase":
                    postQuery.update(accumPrases=F("accumPrases")+1)
                    # 表示当前是已经点赞
                    postDic["isPrased"]=1
                if commentType=="txt":
                    postQuery.update(accumPrases=F("accumContents")+1)

                if commentType=="sound":
                    postQuery.update(accumPrases=F("accumAudios")+1)

                if commentType=="monkey":
                    postQuery.update(accumPrases=F("accumMonkeys")+1)

                post.refresh_from_db()
                self._makeComments(post,postDic,profile)

                # 发送赞扬通知，给被赞扬者
            content["data"]=postDic
        except Exception as e:
            logger.error(e)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult
stageService=StageService()
