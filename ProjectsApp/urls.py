
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project/form$', views.getProjectForm, name='ProjectForm'),
    url(r'^project/formsuccess$', views.getProjectFormSuccess, name='ProjectFormSuccess'),
    url(r'^project/edit$', views.update_profile, name='EditProject'),
    url(r'^project/delete$', views.deleteProject, name='EditProject'),
    url(r'^project/bookmark$', views.bookmark, name='bookmark'),
    url(r'^project/unbookmark$', views.unbookmark, name='unbookmark'),
    url(r'^project/formsuccess$', views.getProjectFormSuccess, name='success'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^project/bookmarks$', views.bookmarks, name='bookmarks'),
]