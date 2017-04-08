from django.shortcuts import render
import sys
import json
import logging
logger = logging.getLogger("django")
from django.views.generic.base import View
from api.service import grainService
# Create your views here.
class GrainFamilyView(View):
    def post(self,req,*arg,**kwargs):
        jsResult=None
        try:
            logger.error(req.user.profile.org.id)
            jsResult= grainService.family(req.user.profile.org)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()

class GrainFamilyAddMemberView(View):
    def post(self,req,*arg,**kwargs):
        logger.error("GrainFamilyAddMemberView")
        reqData=json.loads(str(req.body,'utf-8'))
        childinfo=reqData["childinfo"]
        jsResult=None
        try:
            logger.error(req.user.profile.org.id)
            jsResult= grainService.addmember(req.user.profile.org,childinfo)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()

class GrainFeedbackView(View):
    def post(self,req,*arg,**kwargs):
        logger.error("GrainFeedbackView")
        reqData=json.loads(str(req.body,'utf-8'))
        pid=reqData["pid"]
        role=reqData["role"]
        jsResult=None
        try:
            jsResult= grainService.addmember(req.user.profile.org,int(pid),role)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()

class GrainFamilyGetMemberView(View):
    def post(self,req,*arg,**kwargs):
        logger.error("GrainFamilyGetMemberView")
        reqData=json.loads(str(req.body,'utf-8'))
        childid=reqData["childid"]
        jsResult=None
        try:
            jsResult= grainService.getmember(childid)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()
class GrainFamilyUpdateMemberView(View):
    def post(self,req,*arg,**kwargs):
        logger.error("GrainFamilyUpdateMemberView")
        reqData=json.loads(str(req.body,'utf-8'))
        childinfo=reqData["childinfo"]
        jsResult=None
        try:
            jsResult= grainService.updatemember(childinfo)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()
