from django.db import models
from back.models import EntityBase

# Create your models here.
HONOR_LEVEL_CHOICES = (
    ('B', '体力'),
    ('L', '爱心'),
)
class Honor(EntityBase):
    score=models.IntegerField(verbose_name="分值临界点")
    cat=models.CharField(max_length=4,choices=HONOR_LEVEL_CHOICES,verbose_name="称号分类")
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="A.称号"
        verbose_name_plural="A.称号"


class Params(EntityBase):
    amount_moneyUnit=models.IntegerField(verbose_name="单位货币赠送米粒数量")
    amount_feedUnit=models.IntegerField(verbose_name="奖励米粒最小粒度")
    amount_feeratio=models.IntegerField(verbose_name="费率(千分之几)",default=0)
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="B.系统计算参数"
        verbose_name_plural="B.系统计算参数"
