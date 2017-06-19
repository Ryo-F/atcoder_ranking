# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-19 04:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0006_auto_20170616_0233'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtCoderProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_name', models.CharField(max_length=20)),
                ('task_a', models.CharField(blank=True, max_length=500, null=True)),
                ('task_b', models.CharField(blank=True, max_length=500, null=True)),
                ('task_c', models.CharField(blank=True, max_length=500, null=True)),
                ('task_d', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='result',
            name='result_code',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='result_problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranking.AtCoderProblem'),
        ),
        migrations.CreateModel(
            name='AGCProblem',
            fields=[
                ('atcoderproblem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ranking.AtCoderProblem')),
                ('task_e', models.CharField(blank=True, max_length=500, null=True)),
                ('task_f', models.CharField(blank=True, max_length=500, null=True)),
            ],
            bases=('ranking.atcoderproblem',),
        ),
        migrations.AddField(
            model_name='atcoderproblem',
            name='user',
            field=models.ManyToManyField(to='ranking.User'),
        ),
    ]
