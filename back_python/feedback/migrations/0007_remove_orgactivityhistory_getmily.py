# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-25 13:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0006_auto_20170322_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orgactivityhistory',
            name='getMily',
        ),
    ]
