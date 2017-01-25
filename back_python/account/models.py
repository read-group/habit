from django.db import models
from activity.models import Activity
from habitinfo.models import Habit
from org.models import Profile
from org.models import Org
from feedback.models import FeedBack
# Create your models here.
#交易类型
TRADE_TYPE=(
    ("fee","套餐服务费"),
    ("deposit","押金"),#计入当前参与活动，如果全部打卡，那么全部退还。如果当前无参与活动，那么就不能支付押金。支付押金时，自动按照支付日期以前的打卡次数，返还押金
    ("milyInput","套餐囤米"),
    ("milyInputByDeposit","押金囤米"),
    ("milyOutput","米粒打赏"),
    ("milyOutputByDonate","米粒捐赠"),
    ("feedBack","打卡奖励米粒"),
    ("feedBackReturnDeposit","打卡返还押金"),
    ("aveDeposit","平均分配懒人押金"),
)
#交易账户历史
class Account(models.Model):
    tradeDate=models.DateField(auto_now=True,verbose_name="时间")
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
    # purchaser=models.ForeignKey(
    #     Porfile,
    #     on_delete=models.CASCADE,
    #     verbose_name="购买套餐者"
    # ）
    # depositor=models.ForeignKey(
    #     Porfile,
    #     on_delete=models.CASCADE,
    #     verbose_name="押金者"
    # ）
    # feedbacker=models.ForeignKey(
    #             Porfile,
    #             on_delete=models.CASCADE,
    #             verbose_name="打卡者"
    # ）
    feedback=models.ForeignKey(
            FeedBack,
            on_delete=models.CASCADE,
            verbose_name="打卡信息"
    )

    fee=models.IntegerField(default=0,verbose_name="套餐服务费")
    deposit=models.IntegerField(default=0,verbose_name="囤米押金")#免费套餐使用
    milyInput=models.IntegerField(default=0,verbose_name="套餐囤米")
    milyInputByDeposit=models.IntegerField(default=0,verbose_name="押金囤米")
    milyOutput=models.IntegerField(default=0,verbose_name="米粒打赏")
    milyOutputByDonate=models.IntegerField(default=0,verbose_name="米粒捐赠")
    feedBack=models.IntegerField(default=0,verbose_name="打卡奖励米粒")
    feedBackReturnDeposit=models.IntegerField(default=0,verbose_name="打卡奖励押金")
    aveDeposit=models.IntegerField(default=0,verbose_name="平均分配懒人押金")
    createdTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updatedTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name="账务"
        verbose_name_plural="账务"
