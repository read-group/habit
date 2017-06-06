from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from org.models import Profile,MapEngToRole,Org
from django.core.cache import cache
from school.models import ClassGroup
import logging
import json
from django.db import transaction
from account.models import Account
logger = logging.getLogger("django")
# Create your views here.
# def index(request):
#     return render(request,"front/index.html");
class MainView(TemplateView):
    template_name="front/main.html"
    # def get_context_data(self, **kwargs):
    #     ctx=super(MainView,self).get_context_data(**kwargs)
    #     # ctx["refererUrl"]=self.request.META['HTTP_REFERER']
    #     pathfrom=self.request.GET["pathfrom"];
    #     if pathfrom:
    #         ctx['pt']=pathfrom
    #     else:
    #         ctx['pt']=""
    #     return ctx
    def get_template_names(self):
        logger.error("get_template_names")
        role=self.request.GET["role"];
        if role=="teacher":
            return ["front/tmain.html"]

        return ["front/main.html"]
    @transaction.atomic
    def get(self,request,*args,**kwargs):
        # 获取openid，昵称，头像url,性别等信息
        # 按照openid,去查询profile,如果没有存在，就创建一个user,同时创建一个profile
        # 然后去模拟登录login
        # logger.debug("begin main")
        # # logger.debug(request.user.is_authenticated)
        # if(not request.user.is_authenticated):
        #     userTmp= User.objects.get(pk=72)
        #     login(request,userTmp)
        # return super(MainView,self).get(request,*args,**kwargs)
        if(not request.user.is_authenticated):
            logger.error("not logined=================================")
            fp1=None
            fp2=None
            try:
                role=request.GET["role"];
                # 检查
                if role=="child":
                    # 重定向到学生登录页面,这个url
                     return HttpResponseRedirect("/stlogin")


                code=request.GET["code"];
                wxinfoUrl=settings.WX["WX_AUTH_URL_INFO"].replace("{code}",code);
                # logger.debug(wxinfoUrl)
                import urllib.request
                fp1 = urllib.request.urlopen(wxinfoUrl)
                r1 = fp1.read()
                # logger.debug("data1================")
                # logger.debug(r1)
                decodeJson=json.loads(r1)
                # logger.debug(decodeJson["access_token"])
                # logger.debug(decodeJson["openid"])
                # 按照访问token再去获取用户信息
                userInfoUrl=settings.WX["WX_AUTH_USER_INFO"] % (decodeJson["access_token"],decodeJson["openid"])
                fp2=urllib.request.urlopen(userInfoUrl)
                r2 = fp2.read()
                decodeUserInfoJson=json.loads(r2)
                fp1.close()
                fp2.close()

                # 按照openid查找用户，如果不存在就创建，存在就绕过
                userTry=None
                try:
                    userTry= User.objects.get(username__exact=decodeJson["openid"])
                    profileTmp=userTry.profile
                    if role=="teacher" and profileTmp.role=="1":
                        profileTmp.role="3"
                        profileTmp.save()
                except User.DoesNotExist:
                    if role!="child":
                        # 创建新的用户信息
                        userTry=User.objects.create(username=decodeUserInfoJson["openid"])
                        #创建另一个Profile
                        # 如果role=家长，就创建一个家庭
                        orgC=None
                        if role=="host":
                            orgC=Org.objects.create(code=decodeUserInfoJson["openid"],name=decodeUserInfoJson["nickname"])
                        profile=Profile(nickname=decodeUserInfoJson["nickname"],
                        openid=decodeUserInfoJson["openid"],role=MapEngToRole[role],
                        imgUrl=decodeUserInfoJson["headimgurl"],user=userTry,org=orgC)
                        profile.save()
                        #创建三个个人账户（米仓、现金、押金）
                        accountMily=Account()
                        accountMily.accountType="rice"
                        accountMily.profile=profile
                        accountMily.save()
                        accountCash=Account()
                        accountCash.accountType="cash"
                        accountCash.profile=profile
                        accountCash.save()

                        # 默认创建一个默认孩子的用户
                        # nkname=decodeUserInfoJson["nickname"]+"@子"
                        nkname="修改昵称"
                        userC=User.objects.create(username=decodeUserInfoJson["openid"]+"@")
                        # 查询班级
                        classGroupF=None
                        #创建另一个Profile
                        profileC=Profile(nickname=nkname,role=MapEngToRole["child"],
                        imgUrl=decodeUserInfoJson["headimgurl"],user=userC,org=orgC,childpwd="987654",openid=decodeUserInfoJson["openid"])
                        profileC.save()

                        #创建三个个人账户（米仓、现金、押金）
                        accountMilyC=Account()
                        accountMilyC.accountType="rice"
                        accountMilyC.profile=profileC
                        accountMilyC.save()
                        accountCashC=Account()
                        accountCashC.accountType="cash"
                        accountCashC.profile=profileC
                        accountCashC.save()

                        logger.error("add class before.........")
                        cg=ClassGroup.objects.get(pk=7)
                        profileC.classGroups.add(cg)
                        logger.error("add class after.........")

                finally:
                    #登录
                    # 只要不是学生，就登录
                    if role=="teacher":
                        #重定向到一个老师的main页面
                        login(request,userTry)
                        return super(MainView,self).get(request,*args,**kwargs)
                    else:
                        login(request,userTry)

            except (Exception,) as e:
                logger.error(e)

        else:
            # role=request.GET["role"];
            # rolecode=MapEngToRole[role]
            # if request.user.profile.role!=rolecode:
            #     logout(request)
            #     return HttpResponseRedirect("/")
            logger.error(request.get_full_path())
            logger.error("logined=================================")
            logger.debug(request.user.username)
        # 去微信认证
        # 认证通过后，需要创建用户，并login
        # 重新跳转到本页面
        return super(MainView,self).get(request,*args,**kwargs)
