# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('plugins/', views.plugins, name='plugins'),
    path('download_excel/', views.download_excel, name='download_excel'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('manageplugins/', views.manageplugins, name='manageplugins')
]