"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from models import Group
from django.shortcuts import get_object_or_404
from AuthenticationApp.models import Student, MyUser
from ProjectsApp.models import Project
from . import models
from . import forms

from CommentsApp.models import Comment

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups': groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


def getGroup(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                in_name = request.POST.get('group')
                in_group = models.Group.objects.get(name__exact=in_name)
                new_comment = Comment(comment=form.cleaned_data['comment'],user=request.user,group=in_group)
                new_comment.save()
                is_member = in_group.members.filter(email__exact=request.user.email)
                is_student = request.user.is_student
                users = MyUser.objects.filter(is_student=True)
                members = in_group.members.all()
                comments_list = Comment.objects.filter(group=in_group)
                projects = Project.objects.filter()
                in_projects = in_group.project.all()
                recommended = []
                for pr in projects:
					if in_group.experience_required >= pr.experience:
						recommended.append(pr)
						
                context = {
                    'group': in_group,
                    'userIsMember': is_member,
                    'comments' : comments_list,
                    'is_student': is_student,
                    'projects' : projects,
                    'currentUser' : request.user,
                    'users': users,
                    'members': members,
                    'recommended': recommended,
                    'in_projects': in_projects,
                    'isAdmin' : request.user.is_admin
                }
                return render(request, 'group.html', context)
            else:
                form = forms.CommentForm()
        in_name = request.GET.get('name', 'None')
        try:
        	in_group = models.Group.objects.get(name__exact=in_name)
        except:
        	in_group = " "
        try: 
        	is_member = in_group.members.filter(email__exact=request.user.email)
        except:
        	is_member = " "
        is_student = request.user.is_student
        comments_list = Comment.objects.filter(group=in_group)
        users = MyUser.objects.filter(is_student=True)
        projects = Project.objects.filter()
        members = in_group.members.all()
        in_projects = in_group.project.all()
        recommended = []
        for pr in projects:
					if in_group.experience_required > pr.experience:
						recommended.append(pr)
						
        context = {
            'group': in_group,
            'userIsMember': is_member,
            'comments' : comments_list,
            'is_student': is_student,
            'users' : users,
            'projects' : projects,
            'members': members,
            'recommended' : recommended,
            'currentUser' : request.user,
            'in_projects': in_projects,
            'isAdmin' : request.user.is_admin
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


def getGroupForm(request):
    if request.user.is_authenticated():
        form = forms.GroupForm(request.POST or None)
        if form.is_valid():
            if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                return render(request, 'groupform.html', {'error': 'Error: That Group name already exists!'})
            new_group = models.Group(
            name=form.cleaned_data['name'], description=form.cleaned_data['description'], experience_required=form.cleaned_data['experience_required'])
            new_group.save()
            new_group.members.add(request.user)
            context = {
                'name': form.cleaned_data['name'],
            }
            return render(request, 'groupformsuccess.html', context)
        context = {
            "form": form,
            "page_name": "Create Group",
            "button_value": "Create"
        }
        return render(request, 'groupform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


@login_required
def getEditGroup(request):
    in_name = request.GET.get('name', 'None')
    in_group = models.Group.objects.get(name__exact=in_name)
    form = forms.UpdateForm(request.POST or None, instance=in_group)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, this group is updated!')

    context = {
        "form": form,
        "page_name": "Update Group",
        "button_value": "Update"
    }
    return render(request, 'groupform.html', context)


def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_student = request.user.is_student
        in_group.members.add(request.user)
        in_group.save()
        request.user.group_set.add(in_group)
        request.user.save()
        return HttpResponseRedirect("/group?name="+in_name)
    return render(request, 'autherror.html')


def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_student = request.user.is_student
        in_group.members.remove(request.user)
        in_group.save()
        request.user.group_set.remove(in_group)
        request.user.save()
        return HttpResponseRedirect("/group?name="+in_name)
    return render(request, 'autherror.html')


def deleteGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.delete()
        groups_list = models.Group.objects.all()
        context = {
            'groups': groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


def addMembers(request):
    if request.user.is_authenticated():
    	in_user_id = request.GET.get('id')
        in_user_email = request.GET.get('user')
        in_group_name = request.GET.get('name', 'None')
        user = models.MyUser.objects.get(email=in_user_email)
        in_group = models.Group.objects.get(name__exact=in_group_name)
        in_group.members.add(user)
        in_group.save()
        request.user.group_set.add(in_group)
        request.user.save()
        return HttpResponseRedirect("/group?name="+in_group_name)
    return render(request, 'autherror.html')

def deleteComment(request):
    if request.user.is_authenticated():
        in_comment_id = request.GET.get('id')
        in_group_name = request.GET.get('name', 'None')
        comment = Comment.objects.get(id=in_comment_id)
        comment.delete()
        return HttpResponseRedirect("/group?name="+in_group_name)
    return render(request, 'autherror.html')
    
def selectProject(request):
    if request.user.is_authenticated():
        in_project_id = request.GET.get('id')
        in_project_name = request.GET.get('user', 'None')
        in_group_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_group_name)
        in_group.project.add(Project.objects.get(name__exact=in_project_name))
        in_group.save()
        return HttpResponseRedirect("/group?name="+in_group_name)
    return render(request, 'autherror.html')
