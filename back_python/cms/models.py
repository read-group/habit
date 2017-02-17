from django.db import models
from back.models import EntityBase,ModelSerializableMixin
from media.models import MediaResource
# Create your models here.
class WxWelcome(EntityBase,ModelSerializableMixin):
    desc=models.CharField(max_length=100,verbose_name="概述")
    img=models.ForeignKey(
            MediaResource,
            on_delete=models.CASCADE,
            verbose_name="图片"
    )
