# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniversitiesApp', '0004_auto_20161108_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.CharField(max_length=50, null=True),
        ),
    ]