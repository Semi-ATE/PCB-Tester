# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('invalidpermissions/', views.invalidpermissions, name='invalidpermissions'),
    path('userlist/', views.userlist, name='userlist'),
    path('changepassword/', views.changepassword, name='changepassword'),
]