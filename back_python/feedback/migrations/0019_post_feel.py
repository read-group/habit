# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-16 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0018_post_accumcontents'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='feel',
            field=models.CharField(default='PJ', max_length=4, verbose_name='心情'),
        ),
    ]
