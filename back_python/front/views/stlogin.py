from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from org.models import Profile,MapEngToRole,Org
from django.core.cache import cache
import logging
import json
from django.db import transaction
from django.db.models import Q
from account.models import Account
from org.models import Profile
from django.http import HttpResponseRedirect
logger = logging.getLogger("django")
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");
class StLoginView(TemplateView):
    template_name="front/stlogin.html"

    def get_context_data(self, **kwargs):
        ctx=super(StLoginView,self).get_context_data(**kwargs)
        ctx["loginerror"]=self.err
        return ctx

    def get(self,request,*args,**kwargs):
        self.err=""
        return super(StLoginView,self).get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        #验证
        nickname=request.POST["nickname"]
        pwd=request.POST["password"]
        logger.error(nickname)
        try:
            p=Profile.objects.get(nickname__exact=nickname,Q(childpwd__exact=pwd))
            login(request,p.user)
            return HttpResponseRedirect("/main?role=student")
        except Profile.DoesNotExist:
            logger.error(请检查昵称密码或向家长咨询)
            self.err="请检查昵称密码或向家长咨询"
            return super(StLoginView,self).get(request,*args,**kwargs)
