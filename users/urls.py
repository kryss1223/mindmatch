from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'), # Logged users
    path('settings/', views.user_settings, name='user_settings'),
    path('profile/', views.my_profile, name='user_profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile_view'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('profile/<str:username>/friends/', views.user_friends, name='user_friends'),

]
