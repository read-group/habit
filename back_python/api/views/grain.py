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
