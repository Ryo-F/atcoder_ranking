# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-23 03:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0002_auto_20170623_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]