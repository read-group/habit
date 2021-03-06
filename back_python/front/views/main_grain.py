from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");
import urllib
class GrainView(TemplateView):
    template_name="front/main_grain.html"
    def get_context_data(self, **kwargs):
        ctx=super(GrainView,self).get_context_data(**kwargs)
        # ctx["refererUrl"]=self.request.META['HTTP_REFERER']
        path=self.request.path
        pid=self.request.user.profile.id
        oid=self.request.user.profile.openid
        hostRedirect=settings.WX['WX_APP_REDIRECT'].replace("{role}","host")+"&pathfrom=/main/grain&oid="+oid
        ctx["grainUrl"]=hostRedirect
        return ctx
    def get(self,request,*args,**kwargs):
        return super(GrainView,self).get(request,*args,**kwargs)

class GrainOrderView(TemplateView):
    template_name="front/main_grain_order.html"
    def get(self,request,*args,**kwargs):
        return super(GrainOrderView,self).get(request,*args,**kwargs)

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
class GrainFeedbackNoteView(TemplateView):
    template_name="front/main_grain_feedback_note.html"
    def get(self,request,*args,**kwargs):
        return super(GrainFeedbackNoteView,self).get(request,*args,**kwargs)
