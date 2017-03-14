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
        jsResult=None
        try:
            jsResult= activityService.activitys(skip,limit,req.scheme+"://"+req.META["HTTP_HOST"])
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()

class ActivityDetailView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        try:
            reqData=json.loads(str(req.body,'utf-8'))
            idParam=reqData["id"]
            jsResult=activityService.activityDetail(idParam,req.scheme+"://"+req.META["HTTP_HOST"])
        except:
            info=sys.exc_info()
            logger.error(info)
        return jsResult.renderToJsonResponse()
