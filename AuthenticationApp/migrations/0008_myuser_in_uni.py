# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-29 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0007_auto_20161129_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='in_uni',
            field=models.BooleanField(default=False),
        ),
    ]