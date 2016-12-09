"""GroupsApp Models
Created by Naman Patwari on 10/10/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser
from ProjectsApp.models import Project
# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(MyUser)
    project = models.ManyToManyField(Project,default=None, related_name='project_groups')
    experience_required = models.IntegerField(null=True)
    def __str__(self):
        return self.name
        
    def __str__(self):              #Python 3
        return self.name

    def __unicode__(self):           # Python 2
        return self.name

    def has_perm(self, perm, obj=None):
        return True
        