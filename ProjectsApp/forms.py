
from django import forms

from .models import Project

class ProjectForm(forms.Form):
	name = forms.CharField(label='Project Name', max_length=200)
	description = forms.CharField(label='Describe your project', max_length=10000)
	language= forms.CharField(label='Programming Language', max_length=500)
	experience = forms.IntegerField(label='Years of experience')
	speciality = forms.CharField(label='Speciality', max_length=500)
	

    
class UpdateForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        class Meta:
        	model = Project        
        	fields = ('name', 'description', 'language', 'experience','speciality')
        
    def clean_name(self):            
        return self.initial["name"]        
    def clean_description(self):
        return self.initial["description"]
    def clean_language(self):
        return self.initial["language"]
    def clean_experience(self):
        return self.initial["experience"]
    def clean_first_name(self):
        return self.initial["speciality"]

