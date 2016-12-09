
from django.shortcuts import render

from . import models
from . import forms
from django.contrib import messages
from AuthenticationApp.models import MyUser, Engineer
from CommentsApp.models import Comment
from GroupsApp.models import Group
from CompaniesApp.models import Company
from forms import UpdateForm
#from BookmarksApp.models import Bookmark

def getProjects(request):
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        print(in_name)
        in_project = models.Project.objects.get(name__exact=in_name)
        #Get the user_object by searching for the exact email.
        user_object = models.MyUser.objects.get(email__exact=request.user.email)

        flag = False
        company_name = in_project.company

        if request.user.id == in_project.engineer_id :
            flag = True
        group = False
        groups_list = Group.objects.all()
        for in_group in groups_list:
            if in_group.members.filter(email__exact=request.user.email).exists():
                group = True

            engineer_object = models.Engineer.objects.get(user__exact=request.user)

            engineer_company = engineer_object.company

            project_company = in_project.company

            if (str(engineer_company) == str(project_company)):
                user_can_delete = True
            else:
                user_can_delete = False
  
        context = {
            'project' : in_project,
            'userIsMember': flag,
            'in_group' : group,
            'userCanDelete' : user_can_delete,
        }
        
        return render(request, 'project.html', context)
    return render(request, 'autherror.html')
def getProjectFormSuccess(request):
    if request.user.is_authenticated():
            if request.method == 'POST':
                form = forms.ProjectForm(request.POST)
                print(form.is_valid())
                print(form)
                if form.is_valid():
                    if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
                        return render(request, 'projectform.html', {'error' : 'Error: That Project name already exists!'})
                    engineer = Engineer.objects.get(user__exact=request.user)
                    #engineer = models.Engineer.objects.filter(user_id__exact=request.user.id)
                    company_id = engineer.company
                    new_project = models.Project(name=form.cleaned_data['name'], description=form.cleaned_data['description'], language=form.cleaned_data['language'], experience=form.cleaned_data['experience'], speciality=form.cleaned_data['speciality'], engineer_id= request.user.id)
                    new_project.save()
                    context = {
                        'name' : form.cleaned_data['name'],
                        'experience': form.cleaned_data['experience'],
                    }
                    return render(request, 'projectformsuccess.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')
    
def bookmarkProject(request):
    in_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_name)
    has_bookmarked = models.Bookmarks.objects.filter(project__exact=in_project,user__exact=request.user)
    is_member = in_project.createdBy.filter(email__exact=request.user.email)
    is_engineer = request.user.is_engineer
    comments_list = Comment.objects.all()
    groups_list = Group.objects.all()
    assigned_groups = in_project.project_groups.all()
    context = {
        'project' : in_project,
        'userIsMember': is_member,
        'is_engineer' : is_engineer,
        'comments' : comments_list,
        'groups_list' : groups_list,
        'assigned_groups' : assigned_groups
    }
    if has_bookmarked:
        bookmark = models.Bookmarks.objects.get(user__exact=request.user,project__exact=in_project)
        bookmark.delete()
        messages.success(request, 'Unbookmarked! you have successfully unbookmarked this project!')
        context['has_bookmarked'] = False
    else:
        bookmark = models.Bookmarks(user=request.user,project=in_project)
        bookmark.save()
        messages.success(request, 'Bookmarked! you have successfully bookmarked this project!')
        context['has_bookmarked'] = True

    return render(request, 'project.html',context)


def deleteProject(request): 
    in_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_name)
    in_project.delete()
    projects_list = models.Project.objects.all()
    return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProjectForm(request):
    if request.user.is_authenticated():
            form = forms.ProjectForm(request.POST or None)
            if form.is_valid():
                if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'projectform.html', {'error' : 'Error: That Project name already exists!'})
                new_project = models.Project(name=form.cleaned_data['name'], description=form.cleaned_data['description'],language=form.cleaned_data['language'],experience=form.cleaned_data['experience'],speciality=form.cleaned_data['speciality'])
                new_project.created_at = datetime.datetime.now()
                new_project.updated_at = datetime.datetime.now()

                new_project.save()
                new_project.createdBy.add(request.user)
                # request.user.projects_set.add(new_project)
                new_project.save()
                request.user.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'projectformsuccess.html', context)
            context = {
                "form": form,
                "page_name" : "Create Project",
                "button_value" : "Create"
            }
            return render(request,'projectform.html',context)
    return render(request,'autherror.html')

#@login_required
def editProject(request):
    in_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_name)
    form = forms.UpdateForm(request.POST or None, instance=in_project)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, this project is updated!')

    context = {
        "form" : form,
        "page_name" : "Update Project",
        "button_value" : "Update"
    }
    return render(request, 'projectform.html', context)
    
def bookmark(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Project.objects.get(name__exact=in_name)

        request.user.bookmark.add(in_group)

        is_bookmarked = request.user.bookmark.filter(name__exact=in_name)

        context = {
            'project': in_group,
            'userIsMember': True,
            'bookmarked': is_bookmarked,
        }
        return render(request, 'project.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def unbookmark(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Project.objects.get(name__exact=in_name)

        request.user.bookmark.remove(in_group)

        is_bookmarked = request.user.bookmark.filter(name__exact=in_name)

        context = {
            'project': in_group,
            'userIsMember': True,
            'bookmarked': is_bookmarked,
        }
        return render(request, 'project.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')
    
def bookmarks(request):
    if request.user.is_authenticated():
        projects_list = request.user.bookmark.all()
        context = {
            'projects': projects_list,
            'is_bookmark': True
        }
        return render(request, 'projects.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def update_profile(request):
	form = UpdateForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your project was saved!')

	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)
	
	