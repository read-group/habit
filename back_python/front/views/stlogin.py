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
from account.models import Account
logger = logging.getLogger("django")
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");
class StLoginView(TemplateView):
    template_name="front/stlogin.html"
    def get(self,request,*args,**kwargs):
        return super(StLoginView,self).get(request,*args,**kwargs)
