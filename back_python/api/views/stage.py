from django.shortcuts import render
import sys
import json
import logging
logger = logging.getLogger("django")
from django.views.generic.base import View
from api.service import grainService
from api.service import stageService
# Create your views here.
class StageListView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        reqData=json.loads(str(req.body,'utf-8'))
        pageObj=reqData["pageParam"]
        skip=pageObj["skip"]
        limit=skip+pageObj["limit"]
        pid=reqData["pid"]
        pid
        try:
            logger.error("post view")
            jsResult= stageService.postlist(skip,limit,pid)
        except Exception as e:
            logger.error(e)
        return jsResult.renderToJsonResponse()

class StagePraseView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        reqData=json.loads(str(req.body,'utf-8'))
        postid=reqData["postid"]
        pid
        try:
            jsResult= stageService.prase(postid)
        except Exception as e:
            logger.error(e)
        return jsResult.renderToJsonResponse()
