from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");

class GrainView(TemplateView):
    template_name="front/main_grain.html"
    def get_context_data(self, **kwargs):
        ctx=super(GrainView,self).get_context_data(**kwargs)
        # ctx["refererUrl"]=self.request.META['HTTP_REFERER']
        path=self.request.path
        hostRedirect=settings.WX['WX_APP_REDIRECT'].replace("{role}","host")+"&pathfrom="+path
        encode=urllib.parse.urlencode({'redirect_uri':hostRedirect})
        ctx["grainUrl"]=settings.WX['WX_AUTH_URL_CODE'].replace("{redirect_uri}",encode)
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
