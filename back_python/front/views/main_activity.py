from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
import urllib
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");
import logging
logger = logging.getLogger("django")
class ActivityView(TemplateView):
    template_name="front/main_activity.html"
    def get(self,request,*args,**kwargs):
        return super(ActivityView,self).get(request,*args,**kwargs)

class ActivityDetailView(TemplateView):
    template_name="front/main_activity_detail.html"
    def get_context_data(self, **kwargs):
        ctx=super(ActivityDetailView,self).get_context_data(**kwargs)
        # ctx["refererUrl"]=self.request.META['HTTP_REFERER']
        path=self.request.path
        hostRedirect=settings.WX['WX_APP_REDIRECT'].replace("{role}","host")+path
        ctx["host"]=settings.WX['WX_AUTH_URL_CODE'].replace("{redirect_uri}",urllib.parse.urlencode({'redirect_uri':hostRedirect}))
        return ctx
    def get(self,request,*args,**kwargs):
        return super(ActivityDetailView,self).get(request,*args,**kwargs)
