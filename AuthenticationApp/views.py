"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateForm, TeacherForm, EngineerForm
from .models import MyUser, Student, Teacher, Engineer

# Auth Views

def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if next_url is None:
		next_url = "/"
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			messages.warning(request, 'Invalid username or password.')
			
	context = {
		"form": form,
		"page_name" : "Login",
		"button_value" : "Login",
		"links" : ["register"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index.html')

def auth_register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
			password=form.cleaned_data["password2"], 
			first_name=form.cleaned_data["firstname"], last_name=form.cleaned_data["lastname"])
		new_user.first_name = form.cleaned_data["firstname"]
		new_user.last_name=form.cleaned_data["lastname"]
		new_user.is_student = True
		new_user.user_type = 'student'
		new_user.save()			
		#new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
		#	password=form.cleaned_data["password2"], 
		#	first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'], user_type=form.cleaned_data['usertype'])
		#new_user.save()	
		new_student = Student(user = new_user)
		new_student.university = form.cleaned_data['university'].name
		new_student.save()
		login(request, new_user);	
		messages.success(request, 'Success! Your student account was created.')
	
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
	form = UpdateForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your profile was saved!')

	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)
	
	
def register_teacher(request):
	
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	
	form = TeacherForm(request.POST or None)
	if form.is_valid():
		new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
			password=form.cleaned_data["password2"], 
			first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])
		new_user.first_name = form.cleaned_data["firstname"]
		new_user.last_name=form.cleaned_data["lastname"]
		new_user.is_teacher = True
		new_user.user_type = 'teacher'
		new_user.save()	
		new_teacher = Teacher(user = new_user)
		new_teacher.contact_info = form.cleaned_data['contact_info']
		new_teacher.university = form.cleaned_data['university'].name
		new_teacher.save()
		login(request, new_user);	
		messages.success(request, 'Success! Your teacher account was created.')
	
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)

def register_engineer(request):
	
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	
	form = EngineerForm(request.POST or None)
	if form.is_valid():
		new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
			password=form.cleaned_data["password2"], 
			first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])
		new_user.first_name = form.cleaned_data["firstname"]
		new_user.last_name=form.cleaned_data["lastname"]
		new_user.is_engineer = True
		new_user.user_type = 'engineer'
		new_user.save()	
		new_engineer = Engineer(user = new_user)
		new_engineer.contact_info = form.cleaned_data['contact_info']
		new_engineer.alma_mater = form.cleaned_data['alma_mater']
		new_engineer.about = form.cleaned_data['about']
		new_engineer.company= form.cleaned_data['company'].name
		new_engineer.save()
		login(request, new_user);	
		messages.success(request, 'Success! Your Engineering account was created.')
	
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)
