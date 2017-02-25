from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");

class GrainView(TemplateView):
    template_name="front/main_grain.html"
    def get(self,request,*args,**kwargs):
        return super(GrainView,self).get(request,*args,**kwargs)
