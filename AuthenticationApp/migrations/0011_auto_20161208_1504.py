# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UniversitiesApp', '0005_course_teacher'),
        ('AuthenticationApp', '0010_teacher_university'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='experience',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UniversitiesApp.University'),
        ),
    ]
