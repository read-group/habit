from django.db import models
from django.utils import timezone
from back.models import EntityBase
from org.models import Profile
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
        'Profile',
        on_delete=models.CASCADE,
        verbose_name="创建人"
    )
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="B.班级"
        verbose_name_plural="B.班级"
