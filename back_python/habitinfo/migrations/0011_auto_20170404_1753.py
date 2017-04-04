# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitinfo', '0010_auto_20170329_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='code',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='编码'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='freePraiseMilyUnit',
            field=models.IntegerField(choices=[(10, '10'), (20, '20'), (30, '30'), (40, '40'), (50, '50'), (100, '100'), (200, '200'), (300, '300'), (400, '400'), (500, '500'), (600, '600')], default=0, verbose_name='打卡奖励基数'),
        ),
        migrations.AlterField(
            model_name='habitcatalog',
            name='code',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='编码'),
        ),
    ]