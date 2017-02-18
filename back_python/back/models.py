from django.db import models
from django.utils import timezone
from django.core import serializers
from django.views.generic.base import View
from django.http import JsonResponse
import datetime
# Create your models here.
class EntityBase(models.Model):
    code =models.CharField(max_length=30,verbose_name="编码")
    name = models.CharField(max_length=100,verbose_name="名称")
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        abstract=True


class JsonResult(object):
    def __init__(self,status=0,content=None,rawErr=None,errMsg=None,
    help="status-0 indicate sucess,or 1 indicate fail"):
        self.rtnDic={}
        self.rtnDic["status"]=0
        self.rtnDic["content"]=content
        self.rtnDic["rawErr"]=rawErr
        self.rtnDic["errMsg"]=errMsg
        self.rtnDic["help"]="0:sucess,-1:fail"
    def renderToJsonResponse(self):
        return JsonResponse(self.rtnDic)

class JsonResultMixin(object):
    queryset=None
    def initJsonResult(self):
        self.jsonResult=JsonResult()
        return self.jsonResult
    def getJsonedDataSet(self):
        rtn=None
        toJson=self.getQuerySet()
        print(toJson)
        if type(toJson)==list:
            rtn=serializers.serialize("json", toJson)
        else:
            rtn=serializers.serialize("json", [toJson])
        return rtn
    def getQuerySet(self):
        if queryset is None:
           raise Exception("getQuerySet need implement")
        return queryset

class JsonResultView(View,JsonResultMixin):
    def __init__(self,*arg,**kwargs):
        self.initJsonResult()
        super(JsonResultView,self).__init__(*arg,**kwargs)
    # def toJSON(self):
    #     fields = []
    #     for field in self._meta.fields:
    #         fields.append(field.name)
    #     d = {}
    #     for attr in fields:
    #         if isinstance(getattr(self, attr),datetime.datetime):
    #             d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
    #         elif isinstance(getattr(self, attr),datetime.date):
    #             d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
    #         else:
    #             d[attr] = getattr(self, attr)
    #
    #     import json
    #     return json.dumps(d)
