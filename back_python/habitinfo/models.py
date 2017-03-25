from django.db import models
from back.models import EntityBase
# Create your models here.
HABIT_LEVEL_CHOICES = (
    ('L', '低'),
    ('M', '中'),
    ('H', '高'),
)
HABIT_LEVEL_PRAISE = (
    (100, '100'),
    (200, '200'),
    (300, '300'),
    (400, '400'),
    (500, '500'),
    (600, '600'),
)
class HabitCatalog(EntityBase):
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="A.分类"
        verbose_name_plural="A.分类"

class Habit(EntityBase):
    level=models.CharField(max_length=4,choices=HABIT_LEVEL_CHOICES,verbose_name="难度")
    freePraiseMilyUnit=models.IntegerField(default=0,choices=HABIT_LEVEL_PRAISE,verbose_name="打卡奖励基数")
    freePraiseMilyStep=models.IntegerField(default=0,verbose_name="打卡奖励步进数")
    habitCatalog=models.ForeignKey(
        'HabitCatalog',
        on_delete=models.CASCADE,
        verbose_name="所属分类"
    )
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="B.习惯"
        verbose_name_plural="B.习惯"
        ordering=('code',)
