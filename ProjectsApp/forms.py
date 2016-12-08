
from django import forms

from .models import Project

class ProjectForm(forms.Form):
	name = forms.CharField(label='Project Name', max_length=200)
	description = forms.CharField(label='Describe your project', max_length=10000)
	language= forms.CharField(label='Programming Language', max_length=500)
	experience = forms.IntegerField(label='Years of experience')
	speciality = forms.CharField(label='Speciality', max_length=500)
	
class UpdateForm(forms.ModelForm):

    class Meta:
        model = Project        
        fields = ('name', 'description', 'language', 'experience','speciality')
        widgets = { 
            'description': forms.Textarea()
        }
