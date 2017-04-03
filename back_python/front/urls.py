"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import HomeMobileView,MainView,HomeWxAuthView,ActivityView,ActivityDetailView,GrainView,GrainAddChildView,SnsView,MyView
from .views import GrainEditChildView
from .views import TMainClassMemberView
urlpatterns = [
    url(r'^$', HomeMobileView.as_view(),),
    url(r'^MP_verify_HAONGKquSEXIsxKN.txt$', HomeWxAuthView.as_view(),),
    url(r'^main$', MainView.as_view(),name="main"),
    url(r'^main/activity/([t|h|n]{1})$', ActivityView.as_view(),name="main.activity"),
    url(r'^main/activity/detail/.*$', ActivityDetailView.as_view(),name="main.activity.detail"),
    url(r'^main/grain$', GrainView.as_view(),name="main.grain"),
    url(r'^main/grain/addchild$', GrainAddChildView.as_view(),name="main.grain.addchild"),
    url(r'^main/grain/editchild/.*$', GrainEditChildView.as_view(),name="main.grain.editchild"),
    url(r'^main/sns$', SnsView.as_view(),name="main.sns"),
    url(r'^main/my$', MyView.as_view(),name="main.my"),
    url(r'^tmain/classmember/.*$', TMainClassMemberView.as_view(),name="tmain.classmember"),

]
