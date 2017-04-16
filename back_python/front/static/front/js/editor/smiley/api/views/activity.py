from django.shortcuts import render
import sys
import json
import logging
logger = logging.getLogger("django")
from django.views.generic.base import View

from api.service import activityService
# Create your views here.
class ActivityView(View):
    def post(self,req,*arg,**kwargs):
        reqData=json.loads(str(req.body,'utf-8'))
        skip=reqData["pageParam"]["skip"]
        limit=skip+reqData["pageParam"]["limit"]
        tag=reqData["tag"]
        jsResult=None
        try:
            jsResult= activityService.activitys(skip,limit,req.scheme+"://"+req.META["HTTP_HOST"],tag)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()

class ActivityDetailView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        try:
            reqData=json.loads(str(req.body,'utf-8'))
            logger.error("ActivityDetailView")
            idParam=reqData["id"]
            logger.error(idParam)
            jsResult=activityService.activityDetail(req.user,idParam,req.scheme+"://"+req.META["HTTP_HOST"])
        except Exception as e:
            logger.error(e)
        return jsResult.renderToJsonResponse()

class ActivityJoinlView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        try:
            reqData=json.loads(str(req.body,'utf-8'))
            actId=reqData["actId"]
            cats=reqData["cats"]
            jsResult=activityService.activityJoin(req.user,actId,cats)
        except:
            info=sys.exc_info()
            logger.error(info)
        return jsResult.renderToJsonResponse()

class ActivityLoopCheckView(View):
    def get(self,req,*arg,**kwargs):
        jsResult=None
        try:
            # logger.error("in join....")
            # reqData=json.loads(str(req.body,'utf-8'))
            # actId=reqData["actId"]
            # cats=reqData["cats"]
            logger.error("check service....")
            jsResult=activityService.activityLoopCheck()
        except:
            info=sys.exc_info()
            logger.error(info)
        return jsResult.renderToJsonResponse()
