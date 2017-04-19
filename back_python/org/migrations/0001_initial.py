# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-19 14:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isAccessed', models.BooleanField(default=True, verbose_name='是否通过好友请求')),
            ],
            options={
                'verbose_name_plural': 'C.朋友',
                'verbose_name': 'C.朋友',
            },
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=30, null=True, verbose_name='编码')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatedTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name_plural': 'B.家庭',
                'verbose_name': 'B.家庭',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('openid', models.CharField(blank=True, max_length=128, null=True)),
                ('role', models.CharField(choices=[('1', '家长'), ('2', '老师'), ('3', '家长/老师'), ('4', '孩子')], max_length=2, verbose_name='身份')),
                ('imgUrl', models.CharField(blank=True, max_length=256, null=True)),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatedTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('childpwd', models.CharField(blank=True, max_length=256, null=True)),
                ('classGroups', models.ManyToManyField(to='school.ClassGroup')),
                ('org', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='org.Org', verbose_name='所属家庭')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name_plural': 'A.个人补充信息',
                'verbose_name': 'A.个人补充信息',
            },
        ),
    ]
