#!/usr/bin/env python

from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('search/', views.search, name='search'),
    path('recipes/', views.recipeList, name='recipeList'),
    path('recipe/<int:recipeId>/', views.recipeOverview, name='recipeOverview'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),

    path('accounts/', include('django.contrib.auth.urls')),
]