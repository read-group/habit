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

class GrainAddChildView(TemplateView):
    template_name="front/main_grain_addchild.html"
    def get(self,request,*args,**kwargs):
        return super(GrainAddChildView,self).get(request,*args,**kwargs)
class GrainEditChildView(TemplateView):
    template_name="front/main_grain_editchild.html"
    def get(self,request,*args,**kwargs):
        return super(GrainEditChildView,self).get(request,*args,**kwargs)

class GrainFeedbackView(TemplateView):
    template_name="front/main_grain_feedback.html"
    def get(self,request,*args,**kwargs):
        return super(GrainFeedbackView,self).get(request,*args,**kwargs)
