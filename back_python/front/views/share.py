from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect
import json
import logging
logger = logging.getLogger("django")
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");

class ShareFeedView(TemplateView):
    template_name="front/sharefeed.html"
    def get_context_data(self, **kwargs):
        ctx=super(ShareFeedView,self).get_context_data(**kwargs)
        return ctx

    def get(self,request,*args,**kwargs):
        logger.error("ShareFeedView.............")
        actid=args[0]
        logger.error("ShareFeedView............."+str(actid))
        pid=args[1]
        hid=args[2]
        kwargs["actid"]=actid
        kwargs["pid"]=pid
        kwargs["hid"]=hid
        return super(ShareFeedView,self).get(request,*args,**kwargs)
