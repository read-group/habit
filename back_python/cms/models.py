from django.db import models
from back.models import EntityBase,ModelSerializableMixin
from media.models import MediaResource
# Create your models here.
class WxWelcome(EntityBase,ModelSerializableMixin):
    title=models.CharField(max_length=50,verbose_name="标题")
    desc=models.CharField(max_length=100,verbose_name="概述")
    img=models.ForeignKey(
            MediaResource,
            on_delete=models.CASCADE,
            verbose_name="图片"
    )
