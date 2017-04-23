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
from .views import HomeMobileView,MainView,HomeWxAuthView,ActivityView,ActivityDetailView,GrainView,GrainAddChildView,StageView,MyView
from .views import GrainEditChildView,GrainFeedbackView,GrainFeedbackNoteView
from .views import TMainClassMemberView,TMainAddClassView
from .views import TMyView
from .views import StLoginView
from .views import MyExitView
from .views import MyFriendsView
urlpatterns = [
    url(r'^$', HomeMobileView.as_view(),),
    url(r'^MP_verify_HAONGKquSEXIsxKN.txt$', HomeWxAuthView.as_view(),),
    url(r'^stlogin$', StLoginView.as_view(),name="stlogin"),
    url(r'^main$', MainView.as_view(),name="main"),
    url(r'^main/activity/([t|h|n]{1})$', ActivityView.as_view(),name="main.activity"),
    url(r'^main/activity/detail/.*$', ActivityDetailView.as_view(),name="main.activity.detail"),
    url(r'^main/grain$', GrainView.as_view(),name="main.grain"),
    url(r'^main/grain/addchild$', GrainAddChildView.as_view(),name="main.grain.addchild"),
    url(r'^main/grain/editchild/.*$', GrainEditChildView.as_view(),name="main.grain.editchild"),
    url(r'^main/grain/feedback/note/([0-9]+)$', GrainFeedbackNoteView.as_view(),name="main.grain.feedbacknote"),
    url(r'^main/grain/feedback/([0-9]+)/([0-9]+)', GrainFeedbackView.as_view(),name="main.grain.feedback"),
    url(r'^main/stage/([-1-9]+)$', StageView.as_view(),name="main.stage"),
    url(r'^main/my$', MyView.as_view(),name="main.my"),
    url(r'^main/grain/friends$',MyFriendsView.as_view(),name="main.friends"),
    url(r'^main/exit$', MyExitView.as_view(),name="main.myexit"),
    url(r'^tmain/classmember/.*$', TMainClassMemberView.as_view(),name="tmain.classmember"),
    url(r'^tmain/addclass/$', TMainAddClassView.as_view(),name="tmain.addclass"),
    url(r'^tmain/my$', TMyView.as_view(),name="tmain.my"),

]
