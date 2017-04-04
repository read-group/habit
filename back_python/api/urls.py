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
from api.views import WxWelcomeView,ActivityView,ActivityDetailView,ActivityJoinlView,ActivityLoopCheckView,GrainFamilyView,GrainFamilyAddMemberView
from api.views import GrainFamilyGetMemberView
from api.views import GrainFamilyUpdateMemberView
from api.views import TeacherClassMemberView
from api.views import TeacherMyView
urlpatterns = [
     url(r'^wxwelcome/$',WxWelcomeView.as_view()),
     url(r'^activity/$',ActivityView.as_view()),
     url(r'^activity/detail$',ActivityDetailView.as_view()),
     url(r'^activity/join$',ActivityJoinlView.as_view()),
     url(r'^activity/check$',ActivityLoopCheckView.as_view()),
     url(r'^grain/family$',GrainFamilyView.as_view()),
     url(r'^grain/family/addmember$',GrainFamilyAddMemberView.as_view()),
     url(r'^grain/family/getmember$',GrainFamilyGetMemberView.as_view()),
     url(r'^grain/family/updatemember$',GrainFamilyUpdateMemberView.as_view()),
     url(r'^teacher/classmember$',TeacherClassMemberView.as_view()),
     url(r'^teacher/my$',TeacherMyView.as_view()),
]
