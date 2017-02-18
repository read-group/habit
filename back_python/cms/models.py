from django.db import models
from back.models import EntityBase
from media.models import MediaResource
# Create your models here.
class WxWelcome(EntityBase):
    desc=models.CharField(max_length=100,verbose_name="概述")
    img=models.ForeignKey(
            MediaResource,
            on_delete=models.CASCADE,
            verbose_name="图片"
    )
    class Meta:
        verbose_name="微信欢迎"
        verbose_name_plural="微信欢迎"
