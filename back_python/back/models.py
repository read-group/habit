from django.db import models
from django.utils import timezone
# Create your models here.
class EntityBase(models.Model):
    code =models.CharField(max_length=30,verbose_name="编码")
    name = models.CharField(max_length=100,verbose_name="名称")
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        abstract=True
