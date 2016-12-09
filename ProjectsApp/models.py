"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from AuthenticationApp.models import MyUser, Engineer
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    company = models.CharField(max_length=400, null=True)
    group = models.CharField(max_length=400, null=True)
    language= models.CharField(max_length=500, null=True)
    experience = models.IntegerField(null=True)
    speciality = models.CharField(max_length=500, null=True)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, null=True)
    createdBY =  models.ManyToManyField(MyUser)
 
    def __str__(self):
        return self.name
        
   