from django.shortcuts import render
from api.service import welcomeService
from django.views.generic.base import View
import sys
import json
# Create your views here.
class WxWelcomeView(View):
    def get(self,req,*arg,**kwargs):
        jsResult=None
        try:
            jsResult= welcomeService.welcome(req.scheme+"://"+req.META["HTTP_HOST"])
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()

class LoopHeadView(View):
    def get(self,req,*arg,**kwargs):
        jsResult=None
        try:
            jsResult= welcomeService.loopHead(req.scheme+"://"+req.META["HTTP_HOST"])
        except:
            info=sys.exc_info()
            logging.error(info)
        return jsResult.renderToJsonResponse()
