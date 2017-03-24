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
        logger.error("GrainFamilyView")
        jsResult=None
        try:
            jsResult= grainService.family(req.user.profile.org)
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()
