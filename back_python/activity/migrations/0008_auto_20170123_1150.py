# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0007_activityitem_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='memo',
            field=models.TextField(max_length=200, verbose_name='备注'),
        ),
    ]
