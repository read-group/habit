# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-19 14:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=30, null=True, verbose_name='编码')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatedTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('level', models.CharField(choices=[('L', '低'), ('M', '中'), ('H', '高')], max_length=4, verbose_name='难度')),
                ('freePraiseMilyUnit', models.IntegerField(choices=[(10, '10'), (20, '20'), (30, '30'), (40, '40'), (50, '50'), (100, '100'), (200, '200'), (300, '300'), (400, '400'), (500, '500'), (600, '600')], default=0, verbose_name='打卡奖励基数')),
                ('freePraiseMilyStep', models.IntegerField(default=0, verbose_name='打卡奖励步进数')),
                ('icon', models.CharField(choices=[('fa fa-sun-o fa-lg sun', '生活'), ('fa fa-diamond fa-lg diamond', '诚实'), ('fa fa-share-alt fa-lg', '分享'), ('fa fa-birthday-cake fa-lg thank', '感恩'), ('fa fa-book fa-lg read', '阅读'), ('fa fa-bicycle fa-lg', '运动')], default='fa fa-sun-o sun', max_length=64, verbose_name='图标')),
            ],
            options={
                'ordering': ('code',),
                'verbose_name_plural': 'B.习惯',
                'verbose_name': 'B.习惯',
            },
        ),
        migrations.CreateModel(
            name='HabitCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=30, null=True, verbose_name='编码')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatedTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('forParent', models.BooleanField(default=False, verbose_name='是否父母专用')),
            ],
            options={
                'verbose_name_plural': 'A.分类',
                'verbose_name': 'A.分类',
            },
        ),
        migrations.AddField(
            model_name='habit',
            name='habitCatalog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habitinfo.HabitCatalog', verbose_name='所属分类'),
        ),
    ]
