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
    lazyFund=models.IntegerField(default=0,verbose_name="懒人基金")
    enableLazyFund=models.BooleanField(default=False,verbose_name="是否参与懒人基金")
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

    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name="A.打卡"
        verbose_name_plural="A.打卡"

#打卡的时光记录
class Post(models.Model):
    postDate=models.DateField(auto_now_add=True,verbose_name="发帖日期")
    feedBack=models.ForeignKey(
        FeedBack,
        on_delete=models.CASCADE,
        verbose_name="时光记录"
    )
    content=models.CharField(max_length=150,null=True,blank=True)
    img=models.ForeignKey(
        MediaResource,
        on_delete=models.CASCADE,
        verbose_name="活动"
    )
    accumPrases=models.IntegerField(default=0,verbose_name="累积赞")
    accumAudios=models.IntegerField(default=0,verbose_name="累积语音")
    accumAudios=models.IntegerField(default=0,verbose_name="累积打赏")
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
            verbose_name="活动",
            null=True,
    )
    content=models.CharField(max_length=150,null=True,blank=True)
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name="C.点评"
        verbose_name_plural="C.点评"
