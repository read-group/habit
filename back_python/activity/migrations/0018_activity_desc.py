# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0017_auto_20170305_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='desc',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词'),
        ),
    ]
