from django.db import models
from activity.models import Activity
from habitinfo.models import Habit
from org.models import Profile
from org.models import Org
from media.models import MediaResource
# Create your models here.
#庭习惯历史
#需要计算出某个活动某个家庭需要打卡的次数，按照押金计算每次打卡可以解绑的现金金额，
#平分懒人的奖金
class OrgActivityHistory(models.Model):
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    org=models.ForeignKey(
            Org,
            on_delete=models.CASCADE,
            verbose_name="家庭"
    )
    activity=models.ForeignKey(
            Activity,
            on_delete=models.CASCADE,
            verbose_name="活动"
    )
    # 逗号分割，每个习惯id１:允许请假天数，d２:允许请假天数
    habits=models.CharField(max_length=150,null=True,blank=True,verbose_name="习惯")
    # 活动检查服务，会遍历每个活动历史记录，如果到达结束时间就要设置活动为结束状态
    # 就要检查这个活动的类型，是否是免费，如果是免费，需要
    isFree=models.BooleanField(default=True,verbose_name="是否免费")
    fee=models.IntegerField(default=0,verbose_name="收费金额")
    lazyFund=models.IntegerField(default=0,verbose_name="懒人基金")
    enableLazyFund=models.BooleanField(default=False,verbose_name="是否参与懒人基金")
    activityDays=models.IntegerField(default=0,verbose_name="持续天数")
    def __str__(self):
        return self.activity.name;
    class Meta:
        verbose_name="C.家庭活动历史"
        verbose_name_plural="C.家庭活动历史"
#打卡历史
class FeedBack(models.Model):
    feedDate=models.DateField(auto_now_add=True,verbose_name="打卡日期")
    profile=models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="打卡者"
    )
    orgActivityHistory=models.ForeignKey(
            OrgActivityHistory,
            on_delete=models.CASCADE,
            verbose_name="家庭个人历史习惯",
            null=True
    )
    habit=models.ForeignKey(
            Habit,
            on_delete=models.CASCADE,
            verbose_name="习惯",
            null=True
    )
    freeMily =models.IntegerField(default=0,verbose_name="打卡得米")
    accumDays=models.IntegerField(default=0,verbose_name="累积天数")
    accumMily=models.IntegerField(default=0,verbose_name="累积得米")
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name="A.打卡"
        verbose_name_plural="A.打卡"

#打卡的时光记录
class Post(models.Model):
    postDate=models.DateField(auto_now_add=True,verbose_name="发帖日期")
    feedBack=models.OneToOneField(
        FeedBack,
        on_delete=models.CASCADE,
        verbose_name="时光记录"
    )
    content=models.CharField(max_length=150,null=True,blank=True)
    feel=models.CharField(max_length=4,default="PJ",verbose_name="心情")
    imgUrl=models.CharField(max_length=256,default="http://mily365.com/media/upload/mily.png",verbose_name="反馈图片")
    audioUrls=models.CharField(max_length=1024,default="",verbose_name="音频")
    accumPrases=models.IntegerField(default=0,verbose_name="累积赞")
    accumAudios=models.IntegerField(default=0,verbose_name="累积语音")
    accumMonkeys=models.IntegerField(default=0,verbose_name="累积打赏")
    accumContents=models.IntegerField(default=0,verbose_name="累积内容")
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name="B.发帖"
        verbose_name_plural="B.发帖"

#点评
#点评类型
Comment_TYPE=(
  ("prase","赞扬",),
  ("sound","语音",),
  ("money","打赏",),
)
class Comment(models.Model):
    commentDate=models.DateTimeField(auto_now_add=True,verbose_name="点评日期")
    post=models.ForeignKey(
            Post,
            on_delete=models.CASCADE,
            verbose_name="点评"
    )
    fromProfile=models.ForeignKey(
            Profile,
            on_delete=models.CASCADE,
            verbose_name="点评者"
    )
    commentType=models.CharField(max_length=10,choices=Comment_TYPE)
    audio=models.ForeignKey(
            MediaResource,
            on_delete=models.CASCADE,
            verbose_name="音频",
            null=True,
    )
    content=models.CharField(max_length=150,null=True,blank=True)
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name="C.点评"
        verbose_name_plural="C.点评"
