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
CMS_USAGE = (
    ('0', '移动'),
    ('1', 'ＰＣ'),
)
CMS_STATUS = (
    ('0', '停用'),
    ('1', '启用'),
)
class LoopHead(EntityBase):
    status=models.CharField(max_length=2,default='1',choices=CMS_STATUS,verbose_name="状态")
    usage=models.CharField(max_length=2,default='0',choices=CMS_USAGE,verbose_name="用途")
    name=models.CharField(max_length=100,verbose_name="主题",null=True,blank=True)
    desc=models.CharField(max_length=100,verbose_name="概述",null=True,blank=True)
    imgResource=models.ForeignKey(
            MediaResource,
            on_delete=models.CASCADE,
            verbose_name="图片"
    )
    class Meta:
        verbose_name="首页轮换图"
        verbose_name_plural="首页轮换图"
