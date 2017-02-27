from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");

class ActivityView(TemplateView):
    template_name="front/main_activity.html"
    def get(self,request,*args,**kwargs):
        return super(ActivityView,self).get(request,*args,**kwargs)

class ActivityDetailView(TemplateView):
    template_name="front/main_activity_detail.html"
    def get(self,request,*args,**kwargs):
        return super(ActivityDetailView,self).get(request,*args,**kwargs)
