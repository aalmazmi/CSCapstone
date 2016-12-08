# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 14:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ProjectsApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmarks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='company',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='engineer',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='experience',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='language',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='speciality',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='bookmarks',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ProjectsApp.Project'),
        ),
        migrations.AddField(
            model_name='bookmarks',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
