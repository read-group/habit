# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-22 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MediaResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='名称')),
                ('mediaType', models.CharField(choices=[('img', '图像'), ('audio', '声音'), ('video', '视频')], max_length=50, verbose_name='类型')),
                ('img', models.FileField(upload_to='upload/', verbose_name='文件路径')),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatedTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '媒体文件',
                'verbose_name_plural': '媒体文件',
            },
        ),
    ]
