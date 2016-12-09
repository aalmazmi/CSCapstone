"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from . import models
from . import forms
from AuthenticationApp.models import MyUser, Teacher, Student, Engineer

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
    	teach = False
    	if request.user.is_teacher == True:
    		mon = Teacher.objects.get(user=request.user)
    		if mon.university == request.GET.get('name'):
    			teach = mon
    			in_university = models.University.objects.get(name__exact=request.GET.get('name'))
    			in_university.members.add(request.user)
    			in_university.save()
    			request.user.university_set.add(in_university)
    			request.user.save()
    	if request.user.is_student == True:
    		mon = Student.objects.get(user=request.user)
    		if mon.university == request.GET.get('name'):
    			in_university = models.University.objects.get(name__exact=request.GET.get('name'))
    			in_university.members.add(request.user)
    			in_university.save()
    			request.user.university_set.add(in_university)
    			request.user.save()
        
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
            'teach': teach
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.add(request.user)
        in_university.save();
        request.user.university_set.add(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': True,
        }
        request.user.in_uni = True;
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def getCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		is_member = in_course.members.filter(email__exact=request.user.email)
		students = MyUser.objects.filter(is_student=True)
		if request.user.is_teacher == True:
			teach = Teacher.objects.get(user=request.user)
			if(str(teach) == str(in_course.teacher)):
				course_teach = True
			else:
				course_teach = False
		else:
			course_teach = False
				
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse' : is_member,
			'courseTeacher' : course_teach,
			'students': students
			}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def courseForm(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		context = {
			'university': in_university,
		}
		return render(request, 'courseform.html', context)
    # render error page if user is not logged in
	return render(request, 'autherror.html')

def addCourse(request):
    if request.user.is_authenticated():
    		#use_type = request.user.GET.get('user_type', 'None')
    		
    		if request.user.is_teacher != True :
    			messages.warning(request, 'Not a teacher, cannot add course')
    			return render(request, 'courseform.html', {'error': 'Not a teacher!'})
    			
    		teach = Teacher.objects.get(user=request.user)
    		if request.method == 'POST':
    			form = forms.CourseForm(request.POST)
                if form.is_valid():
                    in_university_name = request.GET.get('name', 'None')
                    in_university = models.University.objects.get(name__exact=in_university_name)
                    if not request.user in in_university.members.all():
                    	messages.warning(request, 'Not in this university!')
                    	return render(request, 'courseform.html', {'error': 'Not a teacher in this university!'})
                    
                    if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
                        return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
                    
                    new_course = models.Course(tag=form.cleaned_data['tag'],
                                               name=form.cleaned_data['name'],
                                               description=form.cleaned_data['description'],
                                               university=in_university,
                                               teacher=teach
                                               )
                    new_course.save()
                    new_course.members.add(request.user)
                    in_university.course_set.add(new_course)
                    is_member = in_university.members.filter(email__exact=request.user.email)
                    teacher = Teacher.objects.get(user=request.user)
                    context = {
                        'university' : in_university,
                        'userIsMember': is_member,
                        'teacher' : teacher,
                    }
                    return render(request, 'university.html', context)
                
                else:
                	return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
            #else:
            #	form = forms.CourseForm()
            #	return render(request, 'courseform.html')
            # render error page if user is not logged in
    return render(request, 'autherror.html')

def manageCourse(request):
	if request.user.is_authenticated():
    		#use_type = request.user.GET.get('user_type', 'None')
    		in_university_name = request.GET.get('name', 'None')
    		in_university = models.University.objects.get(name__exact=in_university_name)
    		in_course_name = request.GET.get('course', 'None')
    		course_obj = models.Course.objects.get(tag__exact=in_course_name)
    		form = forms.CourseUpdate(request.POST)
    		if form.is_valid():
    			update_course = form.save(commit=False)
    			update_course.members.clear()
    			for email in form.cleaned_data['course_members']:
    				student_ob = MyUser.objects.get(email__exact=email)
    				update_course.members.add(student_ob)
    			
    			update_course.save()
    			if (str(Teacher.objects.get(user=request.user)) == str(course_obj.teacher)):
    				teach = True
    			else:
    				teach = False
    				
    		
    			context = {
    			'university' : in_university,
    			'course' : course_obj,
    			'courseTeacher' : Teacher,
    			}
    			
    			return render(request, 'course.html', context)
    		context = {
    			'university' : in_university,
    			'userIsMember': in_university.members.filter(email__exact=request.user.email),
    			'teacher': True,
    		}	
    			
    		return render(request, 'university.html', context)
    	return render(request, 'autherror.html')
    
def removeCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.delete()
		is_member = in_university.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'userIsMember' : is_member,
		}
		return render(request, 'university.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def joinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		if not request.user in in_university.members.all():
			messages.warning(request, 'Not in this university!')
			return render(request, 'autherror.html')
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.add(request.user)
		in_course.save();
		request.user.course_set.add(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': True,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def removeStudent(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_student = request.GET.get('student')
		usez = MyUser.objects.get(email__exact=in_student)
		in_course.members.remove(usez)
		in_course.save();
		usez.course_set.remove(in_course)
		usez.save()
		if request.user.is_teacher == True:
			teach = Teacher.objects.get(user=request.user)
			if(str(teach) == str(in_course.teacher)):
				course_teach = True
			else:
				course_teach = False
		else:
			course_teach = False
				
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse' : True,
			'courseTeacher' : True,
			'students': MyUser.objects.filter(is_student=True)

			}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')
def addStudent(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_student = request.GET.get('student')
		usez = MyUser.objects.get(email__exact=in_student)
		in_course.members.add(usez)
		in_course.save();
		usez.course_set.add(in_course)
		usez.save()
		if request.user.is_teacher == True:
			teach = Teacher.objects.get(user=request.user)
			if(str(teach) == str(in_course.teacher)):
				course_teach = True
			else:
				course_teach = False
		else:
			course_teach = False
				
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse' : True,
			'courseTeacher' : True,
			'students': MyUser.objects.filter(is_student=True)
			}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def unjoinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.remove(request.user)
		in_course.save();
		request.user.course_set.remove(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': False,
			'students': MyUser.objects.filter(is_student=True)

		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')
