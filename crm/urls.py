from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.homepage,name = ''), #homepage is the refrence from the function created in views.py
    path('register', views.register, name = 'register'), #name == route name
    path('my-login', views.my_login, name = 'my-login'),
    path('dashboard', views.dashboard,name = 'dashboard'),
    path('user-logout', views.user_logout,name = 'user-logout'),
    path('create-tasks', views.create_tasks,name = 'create-tasks'),
    path('my-tasks', views.my_tasks,name = 'my-tasks'),
    path('update-tasks/<str:pk>', views.update_tasks,name = 'update-tasks'), #Dynamic URL with a space holder
    path('delete-tasks/<str:pk>', views.delete_tasks,name = 'delete-tasks'), #Dynamic URL with a space holder
    path('profile-management', views.profile_management,name = 'profile-management'),
    path('delete-account', views.delete_account,name = 'delete-account'),


]
