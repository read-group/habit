from django.db import models
from back.models import EntityBase
# Create your models here.
HABIT_LEVEL_CHOICES = (
    ('L', '低'),
    ('M', '中'),
    ('H', '高'),
)
HABIT_LEVEL_PRAISE = (
    (10, '10'),
    (20, '20'),
    (30, '30'),
    (40, '40'),
    (50, '50'),
    (100, '100'),
    (200, '200'),
    (300, '300'),
    (400, '400'),
    (500, '500'),
    (600, '600'),
)
HABIT_ICON_CHOICES = (
    ("fa fa-sun-o fa-lg sun", '生活'),
    ("fa fa-diamond fa-lg diamond", '诚实'),
    ("fa fa-share-alt fa-lg", '分享'),
    ("fa fa-birthday-cake fa-lg thank", '感恩'),
    ("fa fa-book fa-lg read", '阅读'),
    ("fa fa-bicycle fa-lg", '运动'),
)
# 	"life":"fa fa-sun-o sun",
#     "honest":"fa fa-diamond diamond",
#     "share":"fa fa-share-alt",
#     "thank":"fa fa-birthday-cake thank",
#     "read":"fa fa-book read",
# "readCOneHour":"fa fa-book read",
#     "readChengyu":"fa fa-book read",
#     "readEOneHour":"fa fa-book read",
#     "readWord":"fa fa-book read",
#     "pardon":"fa fa-child pardon",
#     "resp":"fa fa-chain",
#     "homework":"fa fa-clock-o",
#     "promise":"fa fa-lock",
#     "dabian":"fa fa-smile-o",
#     "drink":"fa fa-coffee",
#     "fruit":"fa fa-apple",
#     "oldLook":"fa fa-wheelchair",
#     "giftFriend":"fa fa-modx",
#     "sport":"fa fa-bicycle",
#     "word":"fa fa-paint-brush",
#     "cubes":"fa fa-cubes","music":"fa fa-music","picture":"fa fa-picture-o",
#     "fat":"fa fa-flash","daynote":"fa fa-edit",
#     "plantKnow":"fa fa-tree","starKnow":"fa fa-cogs","childDance":"fa fa-child"
class HabitCatalog(EntityBase):
    forParent=models.BooleanField(default=False,verbose_name="是否父母专用")
    question=models.CharField(default='f',max_length=256,verbose_name="了解问题")
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="A.分类"
        verbose_name_plural="A.分类"

class Habit(EntityBase):
    level=models.CharField(max_length=4,choices=HABIT_LEVEL_CHOICES,verbose_name="难度")
    freePraiseMilyUnit=models.IntegerField(default=0,choices=HABIT_LEVEL_PRAISE,verbose_name="打卡奖励基数")
    freePraiseMilyStep=models.IntegerField(default=0,verbose_name="打卡奖励步进数")
    icon=models.CharField(default="fa fa-sun-o sun",max_length=64,choices=HABIT_ICON_CHOICES,verbose_name="图标")
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
