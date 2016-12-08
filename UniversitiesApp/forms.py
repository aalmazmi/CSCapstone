"""
UniversitiesApp Forms

Created by Jacob Dunbar on 11/5/2016.
"""
from django import forms
from .models import Course
from AuthenticationApp.models import Student

class UniversityForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    photo = forms.ImageField(label='Photo')
    description = forms.CharField(label='Description', max_length=300)
    website = forms.CharField(label='Website', max_length = 300)

class CourseUpdate(forms.Form):
	students = Student.objects.all()
	
	course_members = forms.ModelMultipleChoiceField(label='course_members', queryset=students)
	
	class Meta:
		model = Course
		exclude =['university', 'teacher']	
		
class CourseForm(forms.Form):
	tag = forms.CharField(label='Tag', max_length=10)
	name = forms.CharField(label='Name', max_length=50)
	description = forms.CharField(label='Description', max_length=300)

