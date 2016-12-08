from __future__ import unicode_literals

from django.db import models
from AuthenticationApp.models import MyUser

class Comment(models.Model):
    time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    group = models.CharField(max_length=30, default='', null=True)


