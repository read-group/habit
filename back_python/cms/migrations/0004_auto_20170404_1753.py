# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20170219_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxwelcome',
            name='code',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='编码'),
        ),
    ]
