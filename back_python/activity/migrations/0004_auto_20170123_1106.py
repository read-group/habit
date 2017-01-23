# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 03:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20170123_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.BooleanField(default=False, verbose_name='关闭状态'),
        ),
        migrations.AlterField(
            model_name='activityitem',
            name='habitCatalog',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='activity.Activity', verbose_name='习惯类别'),
        ),
    ]
