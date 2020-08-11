# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('plugins/', views.plugins, name='plugins'),
    path('pluginsajax/', views.pluginsajax, name='pluginsajax')
]