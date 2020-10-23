from django.urls import path
from . import views

urlpatterns = [
    path('startup/', views.startup, name='startup'),
]
