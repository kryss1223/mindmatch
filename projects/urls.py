from django.urls import path
from . import views

urlpatterns = [
    path('projectscreate/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/members', views.add_project_members, name='add_members'),
    path('projects/<int:project_id>/remove_member/<int:user_id>/', views.remove_project_member, name='remove_project_member'),



]
