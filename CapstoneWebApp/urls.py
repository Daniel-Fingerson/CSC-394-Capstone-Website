#!/usr/bin/env python

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('search/', views.search, name='search'),
    path('recipes/', views.recipeList, name='recipeList'),
    path('recipe/<int:recipeId>/', views.recipeOverview, name='recipeOverview'),
]