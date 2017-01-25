# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 08:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activity', '0013_auto_20170125_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tradeDate', models.DateField(auto_now=True, verbose_name='时间')),
                ('tradeType', models.CharField(choices=[('fee', '套餐服务费'), ('deposit', '押金'), ('milyInput', '套餐囤米'), ('milyInputByDeposit', '押金囤米'), ('milyOutput', '米粒打赏'), ('milyOutputByDonate', '米粒捐赠'), ('feedBack', '打卡奖励米粒'), ('feedBackReturnDeposit', '打卡返还押金'), ('aveDeposit', '平均分配懒人押金')], max_length=50, verbose_name='类型')),
                ('fee', models.IntegerField(default=0, verbose_name='套餐服务费')),
                ('deposit', models.IntegerField(default=0, verbose_name='囤米押金')),
                ('milyInput', models.IntegerField(default=0, verbose_name='套餐囤米')),
                ('milyInputByDeposit', models.IntegerField(default=0, verbose_name='押金囤米')),
                ('milyOutput', models.IntegerField(default=0, verbose_name='米粒打赏')),
                ('milyOutputByDonate', models.IntegerField(default=0, verbose_name='米粒捐赠')),
                ('feedBack', models.IntegerField(default=0, verbose_name='打卡奖励米粒')),
                ('feedBackReturnDeposit', models.IntegerField(default=0, verbose_name='打卡奖励押金')),
                ('aveDeposit', models.IntegerField(default=0, verbose_name='平均分配懒人押金')),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatedTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Activity', verbose_name='活动')),
            ],
        ),
    ]
