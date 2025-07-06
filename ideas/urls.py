from django.urls import path
from . import views

urlpatterns = [
    path('createidea/', views.create_idea, name='create_idea'),
    path('<int:idea_id>/', views.idea_detail, name='idea_detail'),
    path('delete/<int:idea_id>/', views.idea_delete, name='idea_delete'),
]
