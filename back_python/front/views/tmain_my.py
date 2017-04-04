from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");

class TMyView(TemplateView):
    template_name="front/tmain_my.html"
    def get(self,request,*args,**kwargs):
        return super(TMyView,self).get(request,*args,**kwargs)
