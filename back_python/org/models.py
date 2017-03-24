from django.db import models
from django.utils import timezone
from back.models import EntityBase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from school.models import ClassGroup
# Create your models here.
#家庭
class Org(EntityBase):
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="B.家庭"
        verbose_name_plural="B.家庭"
#1-家长，２－老师，３既是家长也是老师，４是学生
#升级利用用户创建时的信号，来更新user角色
PROFILE_ROLE=(
  ("1","家长"),
  ("2","老师"),
  ("3","家长/老师"),
  ("4","孩子")
)
MapEngToRole={
"host":"1",
"teacher":"2",
"child":"4"
}
class Profile(models.Model):
    nickname=models.CharField(max_length=20,null=True,blank=True)
    openid=models.CharField(max_length=128,null=True,blank=True)
    role=models.CharField(max_length=2,choices=PROFILE_ROLE,verbose_name="身份")
    imgUrl=models.CharField(max_length=256,null=True,blank=True)
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    # disabled=models.BooleanField(default=False,verbose_name="是否禁用")
    user=models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            verbose_name="所属用户",
            null=True
    )
    org=models.ForeignKey(
            Org,
            on_delete=models.CASCADE,
            verbose_name="所属家庭",
            null=True
    )
    classGroup=models.ForeignKey(
            ClassGroup,
            on_delete=models.SET_NULL,
            verbose_name="所属班级",
            null=True
    )
    def __str__(self):
        return self.nickname or self.user.username;
    class Meta:
        verbose_name="A.个人补充信息"
        verbose_name_plural="A.个人补充信息"

# def create_user(sender,instance,created,**kwargs):
#     if(created):
#         user=User()
#         user.profile=instance
#         profile.save()
# pre_save.connect(create_user,sender=Profile)

class Friend(models.Model):
    from_profile=models.ForeignKey(
            Profile,
            on_delete=models.SET_NULL,
            verbose_name="发起者",
            null=True,
            related_name="fromFriendSet"

    ),
    to_profile=models.ForeignKey(
            Profile,
            on_delete=models.SET_NULL,
            verbose_name="接受者",
            null=True,
            related_name="toFriendSet"
    ),
    isAccessed=models.BooleanField(default=True,verbose_name="是否通过好友请求")
