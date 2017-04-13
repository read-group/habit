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
        skip=reqData["pageParam"]["skip"]
        limit=skip+reqData["pageParam"]["limit"]
        try:
            logger.error("post view")
            jsResult= stageService.postlist(skip,limit)
        except Exception as e:
            logger.error(e)
        return jsResult.renderToJsonResponse()