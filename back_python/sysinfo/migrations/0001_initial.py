# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Honor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='编码')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatedTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('score', models.IntegerField(verbose_name='分值临界点')),
                ('cat', models.CharField(choices=[('B', '体力'), ('L', '爱心')], max_length=4, verbose_name='称号分类')),
            ],
            options={
                'verbose_name_plural': '称号',
                'verbose_name': '称号',
            },
        ),
        migrations.CreateModel(
            name='Params',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='编码')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatedTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('amount_MoneyUnit', models.IntegerField(verbose_name='单位货币赠送米粒数量')),
                ('amount_feedUnit', models.IntegerField(verbose_name='奖励米粒最小粒度')),
            ],
            options={
                'verbose_name_plural': '系统计算参数',
                'verbose_name': '系统计算参数',
            },
        ),
    ]
