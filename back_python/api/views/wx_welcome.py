from django.shortcuts import render
from django.http import JsonResponse

class JsonResult(object):
    def __init__(self,status=0,content=None,rawErr=None,errMsg=None,
    help="status-0 indicate sucess,or 1 indicate fail"):
        self.status=0
        self.content=content
        self.rawErr=rawErr
        self.errMsg=errMsg
        self.help="status-0 indicate sucess,or 1 indicate fail"
    def buildRtnData():
        return self



# Create your views here.
class Welcome(object):
    pass
