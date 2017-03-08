from django.shortcuts import render
from activity.models import Activity
from django.conf import settings
from back.models import JsonResultView
import sys
import json
# Create your views here.
class ActivityView(JsonResultView):
    def post(self,req,*arg,**kwargs):
        content={}
        data=[]
        try:
            print(req.body)
            reqData=json.loads(str(req.body,'utf-8'))
            skip=reqData["pageParam"]["skip"]
            limit=skip+reqData["pageParam"]["limit"]
            queryCache=Activity.objects.order_by("createdTime");
            count=queryCache.count();
            acts= queryCache[skip:limit]
            for act in acts:
                dataTmp=self.toJSON(act,["id","name","code","startTime","endTime","desc"])
                dataTmp["img"]=req.scheme+"://"+req.META["HTTP_HOST"]+settings.MEDIA_URL+act.img.img.name
                dataTmp["cat"]=act.get_cat_display()
                data.append(dataTmp)

            # data["name"]=welcome.name
            # data["desc"]=welcome.desc
            # data["img"]=welcome.img.img.name
            # data=self.toJSON(act,["name","code"])
            # data["img"]=req.scheme+"://"+req.META["HTTP_HOST"]+settings.MEDIA_URL+welcome.img.img.name
            # print(data["img"])
            content["total"]=count
            content["data"]=data
        except:
            info=sys.exc_info()
            print(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult.renderToJsonResponse()

class ActivityDetailView(JsonResultView):
    def post(self,req,*arg,**kwargs):
        content={}
        try:
            reqData=json.loads(str(req.body,'utf-8'))
            act= Activity.objects.get(pk=reqData["id"])
            dataTmp=self.toJSON(act,["id","name","code","startTime","endTime","desc",'memo'])
            dataTmp["img"]=req.scheme+"://"+req.META["HTTP_HOST"]+settings.MEDIA_URL+act.img.img.name
            dataTmp["cat"]=act.get_cat_display()

            cats=[]
            for item in act.activeItem_set.all():
                print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
                print(item.cat.name)
                habitCat=self.toJSON(item.cat,["id","name"])
                cats.append(habitCat)
            dataTmp["habitCat"]=cats
            content["data"]=dataTmp
        except:
            info=sys.exc_info()
            print(info)
            self.jsonResult.rtnDic["status"]=-1
        else:
            self.jsonResult.rtnDic["content"]=content
        finally:
            return self.jsonResult.renderToJsonResponse()
