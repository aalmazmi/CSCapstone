# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0011_auto_20161208_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='engineer',
            name='company',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
