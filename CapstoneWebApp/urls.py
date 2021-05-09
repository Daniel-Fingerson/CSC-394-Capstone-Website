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
    path('advancedSearch/', views.advancedQuery, name='advancedQuery'),
    path('ajax_calls/IngredientSearch/', views.autocompleteIngredient, name='autocompleteIngredient'),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipes/', views.userRecipeList, name='userRecipeList'),
    path('recipe/add/<int:recipeId>/<str:recipeName>/', views.addRecipe, name='addRecipe'),
    path('recipe/remove/<int:recipeId>/', views.removeRecipe, name='removeRecipe'),


    path('register/', views.register, name='register'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('social-login/', views.socialLogin, name='socialLogin'),

    #TODO make it have a second url paramaater that corresponds to the user ID (not necessary for testing purposes)
    path('fitbitPage/', views.fitbitPage, name='fitbitPage'),
    
    path('spoonacularEndpoints/', views.spoonacularEndpoints, name='spoonacularEndpoints'),
    
]