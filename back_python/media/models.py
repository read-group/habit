from django.db import models

# Create your models here.
MEDIA_TYPE=(
    ("img","图像"),
    ("audio","声音"),
    ("video","视频")
)
class MediaResource(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True,verbose_name="名称")
    mediaType=models.CharField(max_length=50,choices=MEDIA_TYPE,verbose_name="类型")
    img=models.FileField(upload_to="upload/",verbose_name="文件路径")
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    def __str__(self):
        return self.name or "未命名"
    class Meta:
        verbose_name="媒体文件"
        verbose_name_plural="媒体文件"
