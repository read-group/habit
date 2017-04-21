from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth import login,logout
import json
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");

class MyView(TemplateView):
    template_name="front/main_my.html"
    def get(self,request,*args,**kwargs):
        return super(MyView,self).get(request,*args,**kwargs)

class MyExitView(TemplateView):
    def get(self,request,*args,**kwargs):
        logout(request)
        return  return HttpResponseRedirect("/")
