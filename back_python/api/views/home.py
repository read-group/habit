from django.shortcuts import render
import sys
import json
import logging
logger = logging.getLogger("django")
from django.views.generic.base import View
from api.service import homeService
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
# class GrainFamilyGetMemberView(View):
#     def post(self,req,*arg,**kwargs):
#         logger.error("GrainFamilyGetMemberView")
#         reqData=json.loads(str(req.body,'utf-8'))
#         childid=reqData["childid"]
#         jsResult=None
#         try:
#             jsResult= grainService.getmember(childid)
#         except:
#             info=sys.exc_info()
#             logging.error(info)
#         return jsResult.renderToJsonResponse()
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
