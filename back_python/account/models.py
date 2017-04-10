from django.db import models
from activity.models import Activity
from habitinfo.models import Habit
from org.models import Profile
from org.models import Org
from feedback.models import FeedBack
import logging
logger = logging.getLogger("django")
# Create your models here.
#交易类型
TRADE_TYPE=(
    ("fee","套餐服务费"),
    ("deposit","押金"),#计入当前参与活动，如果全部打卡，那么全部退还。如果当前无参与活动，那么就不能支付押金。支付押金时，自动按照支付日期以前的打卡次数，返还押金
    ("milyOutput","米粒打赏"),
    ("milyOutputByDonate","米粒捐赠"),
    ("feedBackMilyInput","打卡奖励米粒"),
    ("feedBackReturnDeposit","打卡返还押金"),
    ("aveDeposit","平均分配懒人押金"),
    ("takeCash","用户提现"),
)
MAP_TRADE_TYPE={
   "feedBackMilyInput":"feedBackMilyInput"
}
SYS_TRADE_TYPE=(
  ("sysFillMily","平台生产米粒"),
  ("sysFreeOutMily","平台免费赠送米粒"),
  ("sysFreeInputMily","平台免费赠送退回米粒"),
  ("sysTakeCash","平台提现"),
  ("sysInitCash","平台预存"),
)
MAP_SYS_TRADE_TYPE={
 "sysFreeOutMily":"sysFreeOutMily"
}
#账户类型
ACCOUNT_TYPE=(
  ("cash","现金"),
  ("rice","米粒"),
  ("deposit","押金"),
)
MAP_ACCOUNT_TYPE={
   "rice":"rice"
}
#
#系统账户
class SysAccount(models.Model):
    name=models.CharField(max_length=50,verbose_name="账户名称")
    accountType=models.CharField(max_length=50,choices=ACCOUNT_TYPE,verbose_name="账户类型")
    balance=models.DecimalField(verbose_name="余额", max_digits=20, decimal_places=2,default=0)
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    def __str__(self):
        return self.name;
    class Meta:
        verbose_name="系统账户"
        verbose_name_plural="系统账户"
#系统账户历史,后台直接操作影响系统账户
class SysAccountHistory(models.Model):
    tradeDate=models.DateTimeField(auto_now_add=True,verbose_name="时间")
    tradeType=models.CharField(max_length=50,choices=SYS_TRADE_TYPE,verbose_name="类型")
    tradeAmount=models.DecimalField(verbose_name="交易额",max_digits=20, decimal_places=2,default=0)
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    sysAccount=models.ForeignKey(
        SysAccount,
        on_delete=models.CASCADE,
        verbose_name="系统账户"
    )
    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        if len(values) != len(cls._meta.concrete_fields):
            values = list(values)
            values.reverse()
            values = [
                values.pop() if f.attname in field_names else DEFERRED
                for f in cls._meta.concrete_fields
            ]
        instance = cls(*values)
        instance._state.adding = False
        instance._state.db = db
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        return instance
    def save(self, *args, **kwargs):
        if self._state.adding:
           self.sysAccount.balance+=self.tradeAmount
        else:
            self.sysAccount.balance-=self._loaded_values['tradeAmount'];
            self.sysAccount.balance+=self.tradeAmount
        logger.error(self.sysAccount.balance);
        self.sysAccount.save()
        super(SysAccountHistory,self).save(*args, **kwargs)
    class Meta:
        verbose_name="系统账务"
        verbose_name_plural="系统账务"
#账户余额,个人钱包
#用户微信认证通过，自动创建两个账户
class Account(models.Model):
    accountType=models.CharField(max_length=50,choices=ACCOUNT_TYPE,verbose_name="账户类型")
    balance=models.DecimalField(verbose_name="余额", max_digits=20, decimal_places=2,default=0)
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    profile=models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="用户",
        null=True
    )
    def __str__(self):
        return self.profile.nickname;
    class Meta:
        verbose_name="个人钱包"
        verbose_name_plural="个人钱包"
#交易账户历史
class AccountHistory(models.Model):
    tradeDate=models.DateTimeField(auto_now=True,verbose_name="时间")
    tradeType=models.CharField(max_length=50,choices=TRADE_TYPE,verbose_name="类型")
    activity=models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        verbose_name="活动"
    )
    org=models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        verbose_name="家庭"
    )
    operator=models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="责任人"
    )
    account=models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name="个人钱包",
        null=True
    )
    sysAccountHistory=models.ForeignKey(
        SysAccountHistory,
        on_delete=models.CASCADE,
        verbose_name="平台账务",
        null=True
    )
    feedback=models.ForeignKey(
            FeedBack,
            on_delete=models.CASCADE,
            verbose_name="打卡信息"
    )
    fee=models.DecimalField(verbose_name="套餐服务费",max_digits=10, decimal_places=2,default=0)
    tradeAmount=models.DecimalField(verbose_name="交易额",max_digits=20, decimal_places=2,default=0)
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")

    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        if len(values) != len(cls._meta.concrete_fields):
            values = list(values)
            values.reverse()
            values = [
                values.pop() if f.attname in field_names else DEFERRED
                for f in cls._meta.concrete_fields
            ]
        instance = cls(*values)
        instance._state.adding = False
        instance._state.db = db
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        return instance
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.account.balance+=self.tradeAmount
        else:
            self.account.balance-=self._loaded_values['tradeAmount'];
            self.account.balance+=self.tradeAmount
        logger.error(self.account.balance);
        self.account.save()
        super(AccountHistory,self).save(*args, **kwargs)

    class Meta:
        verbose_name="个人账务"
        verbose_name_plural="个人账务"
