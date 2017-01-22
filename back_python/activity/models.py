from django.db import models
from habitinfo.models import HabitCatalog
from back.models import EntityBase

# Create your models here.
ACTIVITY_CAT_CHOICES = (
    ('FEE', '收费'),
    ('FREE', '免费'),#押金赠米，完成了返还押金或者只计算体力值
    ('DONATE', '捐赠'),#押金赠米，完成了返还押金或者只计算体力值
)
class Activity(EntityBase):
    startTime=models.DateField(verbose_name="开始日期")
    endTime=models.DateField(verbose_name="结束日期")
    cat=models.CharField(max_length=20,choices=ACTIVITY_CAT_CHOICES ,verbose_name="类别")
    img=models.ImageField(upload_to="/media",verbose_name="活动图片")
    amount=models.IntegerField(default=0,verbose_name="报名费")
    memo=models.TextField(max_length=500,verbose_name="备注")
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="活动"
        verbose_name_plural="活动"

class ActivityItem(EntityBase):
    habitCatalog=models.ForeignKey(Activity,verbose_name="习惯类别")
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="活动项目"
        verbose_name_plural="活动项目"
