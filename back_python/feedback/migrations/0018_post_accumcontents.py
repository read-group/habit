# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-14 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0017_auto_20170413_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='accumContents',
            field=models.IntegerField(default=0, verbose_name='累积内容'),
        ),
    ]
