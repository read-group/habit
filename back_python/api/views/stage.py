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
            jsResult= stageService.postlist(skip,limit,pid,req.user.profile)
        except Exception as e:
            logger.error(e)
        return jsResult.renderToJsonResponse()

class StagePraseView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        reqData=json.loads(str(req.body,'utf-8'))
        logger.error("StagePraseView..........")
        # postid=reqData["postid"]
        # commentType=reqData["type"]
        try:
            jsResult= stageService.comment(req.user.profile,reqData)
        except Exception as e:
            logger.error(e)
        return jsResult.renderToJsonResponse()

class TxtNoteView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        reqData=json.loads(str(req.body,'utf-8'))
        logger.error("TxtNoteView..........")
        # postid=reqData["postid"]
        # commentType=reqData["type"]
        try:
            jsResult= stageService.comment(req.user.profile,reqData)
        except Exception as e:
            logger.error(e)
        return jsResult.renderToJsonResponse()

class StageAudioView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        reqData=json.loads(str(req.body,'utf-8'))
        logger.error("StageAudioView..........")
        # postid=reqData["postid"]
        # commentType=reqData["type"]
        try:
            jsResult= stageService.comment(req.user.profile,reqData)
        except Exception as e:
            logger.error(e)
        return jsResult.renderToJsonResponse()
