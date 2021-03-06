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
from api.views import ActivityView,ActivityDetailView,ActivityJoinlView,ActivityLoopCheckView,GrainFamilyView,GrainFamilyAddMemberView
from api.views import GrainFamilyGetMemberView
from api.views import GrainFamilyUpdateMemberView
from api.views import GrainFriendsView
from api.views import GrainFeedbackView
from api.views import GrainFeedbackCreateView,GrainFeedbackPublishView,GrainFeedbackCancelView,GrainFeedbackMilyOrderView
from api.views import TeacherClassMemberView,TeacherAddClassView
from api.views import TeacherMyView,HomeMyView
from api.views import StageListView
from api.views import StagePraseView
from api.views import TxtNoteView,StageAudioView
from api.views import WxWelcomeView,LoopHeadView
from api.views import ShareMyView
urlpatterns = [
     url(r'^wxwelcome/$',WxWelcomeView.as_view()),
     url(r'^welcome/loopHead$',LoopHeadView.as_view()),
     url(r'^activity/$',ActivityView.as_view()),
     url(r'^activity/detail$',ActivityDetailView.as_view()),
     url(r'^activity/join$',ActivityJoinlView.as_view()),
     url(r'^activity/check$',ActivityLoopCheckView.as_view()),
     url(r'^grain/family$',GrainFamilyView.as_view()),
     url(r'^grain/friends$',GrainFriendsView.as_view()),
     url(r'^grain/family/addmember$',GrainFamilyAddMemberView.as_view()),
     url(r'^grain/family/getmember$',GrainFamilyGetMemberView.as_view()),
     url(r'^grain/family/updatemember$',GrainFamilyUpdateMemberView.as_view()),
     url(r'^grain/feedback/habits$',GrainFeedbackView.as_view()),
     url(r'^grain/feedback/create$',GrainFeedbackCreateView.as_view()),
     url(r'^grain/feedback/cancel$',GrainFeedbackCancelView.as_view()),
     url(r'^grain/feedback/publish$',GrainFeedbackPublishView.as_view()),
     url(r'^grain/feedback/milyorder$',GrainFeedbackMilyOrderView.as_view()),
     url(r'^stage/posts$',StageListView.as_view()),
     url(r'^stage/prase$',StagePraseView.as_view()),
     url(r'^stage/txtnote$',TxtNoteView.as_view()),
     url(r'^stage/audio$',StageAudioView.as_view()),
     url(r'^teacher/classmember$',TeacherClassMemberView.as_view()),
     url(r'^teacher/addclass$',TeacherAddClassView.as_view()),
     url(r'^home/my$',HomeMyView.as_view()),
     url(r'^share/feedback$',ShareMyView.as_view()),
     url(r'^teacher/my$',TeacherMyView.as_view()),
]
