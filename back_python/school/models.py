from django.db import models
from django.utils import timezone
from back.models import EntityBase
from django.contrib.auth.models import User
# Create your models here.
class School(EntityBase):
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="A.学校"
        verbose_name_plural="A.学校"

class ClassGroup(EntityBase):
    school=models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        verbose_name="所属学校"
    )
    creator=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="创建者",
        null=True
    )
    imgUrl=models.CharField(max_length=256,null=True,blank=True)
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="B.班级"
        verbose_name_plural="B.班级"
