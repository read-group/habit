from django.db import transaction
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.models import User
from org.models import Profile,MapEngToRole,Org,Friend,MapRoleToEng
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
                queryCache=Post.objects.select_related('feedBack').order_by("-createdTime");
            elif int(pid)==-2:
                queryCache=Post.objects.select_related('feedBack').filter(feedBack__profile__org__id=currentUser.org.id).order_by("-createdTime");
            else:
                queryCache=Post.objects.select_related('feedBack').filter(feedBack__profile__id=int(pid)).order_by("-createdTime");
            count=queryCache.count();
            posts= queryCache[skip:limit]
            for post in posts:
                dataTmp=self.toJSON(post,["id","content","imgUrl","audioUrls","accumPrases","accumContents","accumAudios"])
                dataTmp["postDate"]=post.createdTime.strftime("%Y/%m/%d %H:%M:%S")
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

            if comment.commentType=="txt" or comment.commentType=="sound":
                txtinfoTmp={}
                txtinfoTmp['nickname']=comment.fromProfile.nickname
                txtinfoTmp['imgUrl']=comment.fromProfile.imgUrl
                txtinfoTmp['content']=comment.content
                txtinfoTmp['audioUrl']=comment.audioUrls
                txtinfoTmp['accumAudios']=post.accumAudios
                txtinfoTmp['accumContents']=post.accumContents
                if comment.commentType=="txt":
                    txtinfoTmp["type"]="txt"
                else:
                    txtinfoTmp["type"]="sound"
                txtInfos.append(txtinfoTmp)
            # if comment.commentType=="sound":
            #     soundinfoTmp={}
            #     soundinfoTmp['nickname']=comment.fromProfile.nickname
            #     soundinfoTmp['imgUrl']=comment.fromProfile.imgUrl
            #     soundinfoTmp['audioUrl']=comment.audioUrls
            #     audioInfos.append(soundinfoTmp)
            if comment.commentType=="money":
                moneyinfoTmp={}
                moneyinfoTmp['imgUrl']=comment.fromProfile.imgUrl
                moneyInfos.append(moneyinfoTmp)

        postDic["praseInfos"]=praseInfos
        postDic["txtInfos"]=txtInfos
        # postDic["audioInfos"]=audioInfos
        postDic["moneyInfos"]=moneyInfos
        return postDic

    def comment(self,profile,reqData):
        postid=reqData["postid"]
        commentType=reqData["type"]
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
                if "content" in reqData.keys():
                    comment.content=reqData["content"]
                else:
                    # 给个缺省值
                    comment.content='d'
                if "audiourl" in reqData.keys():
                    comment.audioUrls=reqData["audiourl"]
                comment.save()
                # 增加帖子上的赞扬次数
                if commentType=="prase":
                    postQuery.update(accumPrases=F("accumPrases")+1)
                    # 表示当前是已经点赞
                    postDic["isPrased"]=1
                    # 加好友
                    postCreator=post.feedBack.profile
                    if postCreator.id!=profile.id:
                        # 检查是否已经成为朋友，如果已经成为朋友，那么无需再去创建
                        rawsql="select id,count(id) as ct from org_friend where ( fromp_id=%s and top_id=%s ) or ( fromp_id=%s and top_id=%s )"
                        c=Friend.objects.raw(rawsql,[str(profile.id),str(postCreator.id),str(postCreator.id),str(profile.id)])[0]
                        logger.error("Q ok")
                        if c.ct==0:
                            friends=Friend()
                            friends.fromp=profile
                            friends.top=postCreator
                            friends.save()
                    # 给被赞者发送通知
                    # 发送赞扬通知，给被赞扬者
                    try:
                        import urllib.request
                        import json
                        from django.conf import settings
                        body={}
                        data={
                            "first": {
                            "value":profile.nickname+"刚刚赞了"+postCreator.nickname+"的打卡",
                            "color":"#173177"
                            },
                            "keyword1": {
                            "value":"米粒点赞",
                            "color":"#173177"
                            },
                            "keyword2": {
                            "value":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "color":"#173177"
                            },
                            "remark": {
                            "value":"点击按路径'米粒习惯/我的/时光足迹'查看朋友点赞",
                            "color":"#173177"
                            }
                        };
                        body["touser"]=postCreator.openid
                        body["data"]=data
                        body["tid"]=settings.WX["Tmpid1"]
                        # 当前角色
                        # 获取当前登录人员的角色
                        eng=MapRoleToEng[profile.role]
                        body["queryStr"]="http://mily365.com?role="+eng+"&pathfrom=/main/stage/"+postCreator.id
                        jdata = json.dumps(body)
                        headers={'Content-Type':'application/json'}
                        request2=urllib.request.Request("http://wx.mily365.com/wx/api/sendMsg", jdata.encode('utf-8'),headers)
                        fp1 = urllib.request.urlopen(request2)
                        r2=fp1.read()
                        fp1.close()
                    except Exception as e:
                        logger.error(e)
                        jsonResult.rtnDic["status"]=-1

                if commentType=="txt":
                    postQuery.update(accumContents=F("accumContents")+1)

                if commentType=="sound":
                    postQuery.update(accumAudios=F("accumAudios")+1)

                if commentType=="monkey":
                    postQuery.update(accumMonkeys=F("accumMonkeys")+1)

                post.refresh_from_db()
                self._makeComments(post,postDic,profile)



            content["data"]=postDic
        except Exception as e:
            logger.error(e)
            jsonResult.rtnDic["status"]=-1
        else:
            jsonResult.rtnDic["content"]=content
        finally:
            return jsonResult
stageService=StageService()
