from django.shortcuts import render
import sys
import json
import logging
logger = logging.getLogger("django")
from django.views.generic.base import View
from api.service import homeService
from api.service import feedbackService
# Create your views here.
class HomeMyView(View):
    def post(self,req,*arg,**kwargs):
        logger.error("HomeMyView")
        jsResult=None
        try:
            jsResult= homeService.myfunc(req.user)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()
#
class ShareMyView(View):
    def post(self,req,*arg,**kwargs):
        logger.error("ShareMyView")
        reqData=json.loads(str(req.body,'utf-8'))
        actid=reqData["actid"]
        pid=reqData["pid"]
        hid=reqData["habitid"]
        jsResult=None
        try:
            jsResult= feedbackService.getShareFeedInfo(actid,pid,hid)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()
# class GrainFamilyUpdateMemberView(View):
#     def post(self,req,*arg,**kwargs):
#         logger.error("GrainFamilyUpdateMemberView")
#         reqData=json.loads(str(req.body,'utf-8'))
#         childinfo=reqData["childinfo"]
#         jsResult=None
#         try:
#             jsResult= grainService.updatemember(childinfo)
#         except:
#             info=sys.exc_info()
#             logging.error(info)
#         return jsResult.renderToJsonResponse()
