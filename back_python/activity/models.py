from django.db import models
from habitinfo.models import HabitCatalog
from back.models import EntityBase
from media.models import MediaResource
from school.models import School

# Create your models here.
ACTIVITY_CAT_CHOICES = (
    ('FEE', '收费'),
    ('FREE', '免费'),#押金赠米，完成了返还押金或者只计算体力值
    ('DONATE', '捐赠'),#押金赠米，完成了返还押金或者只计算体力值
    ('Market', '市场'),#重点表扬
)
# Create your models here.
ACTIVITY_STATUS = (
    (0, '未开始'),
    (1, '进行中'),
    (-1, '已结束'),
)
ACTIVITY_LAZY_UNIT = (
    (1, '1元'),
    (2, '２元'),
    (3, '３元'),
    (5, '５元'),
    (8, '８元'),
    (10, '10元'),
)
class Activity(EntityBase):
    startTime=models.DateTimeField(verbose_name="开始日期")
    endTime=models.DateTimeField(verbose_name="结束日期")
    cat=models.CharField(max_length=20,choices=ACTIVITY_CAT_CHOICES ,verbose_name="类别")
    desc=models.CharField(max_length=20,verbose_name="关键词",null=True)
    #img=models.ImageField(upload_to="upload/",verbose_name="活动图片")
    img=models.ForeignKey(
            MediaResource,
            on_delete=models.CASCADE,
            verbose_name="图片"
    )
    applyNumber=models.IntegerField(default=0,verbose_name="已报名人数",editable=False)
    uplimit=models.IntegerField(default=0,verbose_name="人数上限")
    amount=models.IntegerField(default=0,verbose_name="报名费")
    rtnLazyUnit=models.IntegerField(default=1,choices=ACTIVITY_LAZY_UNIT,verbose_name="每日打卡返回押金")
    lazyFund=models.IntegerField(default=0,verbose_name="懒人基金")
    lazyJoinNumber=models.IntegerField(default=0,verbose_name="已经参与懒人计划人数")
    days=models.IntegerField(default=0,verbose_name="活动天数")
    status=models.IntegerField(default=0,choices=ACTIVITY_STATUS,verbose_name="活动状态")
    isTop=models.BooleanField(default=False,verbose_name="是否置顶")
    memo=models.TextField(max_length=4096,verbose_name="注意事项")
    school=models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        verbose_name="发起机构",
        null=True
    )
    def save(self, *args, **kwargs):
        if self._state.adding:
            pass
        else:
            self.days=(self.endTime-self.startTime).days+1
            self.lazyFund=self.days * self.rtnLazyUnit
        super(Activity,self).save(*args, **kwargs)

    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="活动"
        verbose_name_plural="活动"

class ActivityItem(models.Model):
    #activity=models.ForeignKey(Activity,on_delete=models.CASCADE，verbose_name="活动")
    #cat=models.ForeignKey(HabitCatalog,on_delete=models.CASCADE，verbose_name="习惯类别")
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    activity=models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
        verbose_name="活动"
    )
    cat=models.ForeignKey(
        HabitCatalog,
        on_delete=models.SET_NULL,
        verbose_name="习惯类别",
        null=True,
    )
    exceptionCount=models.IntegerField(default=0,verbose_name="允许请假天数")
    def __str__(self):
        return self.cat.name if self.cat is not None else "";
    class Meta:
        verbose_name="活动项目"
        verbose_name_plural="活动项目"
