# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-19 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0008_auto_20170619_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='answered_problem',
            field=models.ManyToManyField(blank=True, to='ranking.AtCoderProblem'),
        ),
    ]