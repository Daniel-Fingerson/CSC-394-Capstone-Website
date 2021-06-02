#!/usr/bin/env python

from django.urls import path
from django.conf.urls import include, url

from . import views


#Formatting note for 'path'
#   arg1: absolute url path after base url (capstonewebiste.ngrok.io/<arg1>)
#   arg2: link to the corresponding backend logic defined in views.py (html file render path + general logic)
#   arg3: variable name for system wide access of the given url

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('search/', views.search, name='search'),
    path('recipes/', views.recipeList, name='recipeList'),
    path('recipe/<int:recipeId>/', views.recipeOverview, name='recipeOverview'),

    


    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipes/', views.userRecipeList, name='userRecipeList'),
    path('recipe/add/<int:recipeId>/<str:recipeName>/', views.addRecipe, name='addRecipe'),
    path('recipe/remove/<int:recipeId>/', views.removeRecipe, name='removeRecipe'),


    path('register/', views.register, name='register'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('userPrefs/', views.prefPage, name = 'preferences'),




    #Future features (not fully implemented)
    path('userMeal/', views.prefPage, name = 'mealPlan'),
    path('userShop/', views.prefPage, name = 'shoppingList'),

    path('advancedSearch/', views.advancedQuery, name='advancedQuery'),
    
    path('ajax_calls/IngredientSearch/', views.autocompleteIngredient, name='autocompleteIngredient'),
    path('ajax_calls/RecipeSearch/', views.autocompleteRecipe, name='autocompleteRecipe'),

    path('social-auth/', include('social_django.urls', namespace="social")),
    path('social-login/', views.socialLogin, name='socialLogin'),

    
    path('fitbitPage/', views.fitbitPage, name='fitbitPage'),
    path('spoonacularEndpoints/', views.spoonacularEndpoints, name='spoonacularEndpoints'),
    
]