from django.db import models

# Create your models here.
class EntityBase(models.Model):
    code =models.CharField(max_length=30,verbose_name="编码")
    name = models.CharField(max_length=100,verbose_name="名称")
    class Meta:
        abstract=True

class School(EntityBase):
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="学校"
        verbose_name_plural="学校"

class ClassGroup(EntityBase):
    school=models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        verbose_name="所属学校"
    )
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="班级"
        verbose_name_plural="班级"
