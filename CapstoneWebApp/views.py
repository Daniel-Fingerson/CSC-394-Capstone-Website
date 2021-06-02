from django.shortcuts import render, redirect
from CapstoneWebApp.forms import RegisterForm, UserPref
from django.contrib.auth import login
from django.urls import reverse

from bootstrap_modal_forms.generic import BSModalCreateView

from CapstoneWebApp.models import Profile
from CapstoneWebApp.models import Recipe as dbRecipe


import fitbit
import CapstoneWebApp.gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import re


from django.http import HttpResponse

import requests



#custom spoonacular API from PyPy rewritten to accomodate more endpoints
import CapstoneWebApp.spoonacular.api as sp


#spoonacular API access key (future version save via secure system variable)
api = sp.API("e49afb82519a407db4b10de35ddf7252")

#Wrapper class for spoonacular for transmitting advanced queries to Spoonacular's API endpoint
from CapstoneWebApp.classes import ComplexSearch


#available Spoonacular cuisine search types
cuisineDefs = [
"African","American",
"British",
"Cajun","Caribbean","Chinese",
"Eastern European","European",
"French",
"German","Greek"
"Indian","Irish","Italian",
"Japanese","Jewish",
"Korean",
"Latin American",
"Mediterranean","Mexican","Middle Eastern",
"Nordic",
"Southern","Spanish",
"Thai",
"Vietnamese"
]

#available Spoonacular diet types (accompnaying description is stored within models.py)
dietDefs = [
"Gluten Free",
"Ketogenic",
"Vegetarian",
"Lacto-Vegetarian",
"Ovo-Vegetarian",
"Vegan",
"Pescetarian",
"Paleo",
"Primal",
"Whole30"
]



def index(request):
	''' Index page of site '''
	if request.method == "GET":
		print("its a get request")
	elif request.method == "POST":
		print("its a post request (most likely an Ouath redriect )")
	return render(request, rootDir+'index.html')


def test(request):
	''' Test page of site (quick rendering/JS functionality tests) '''
	response = api.parse_ingredients("3.5 cups King Arthur flour", servings=1)
	data = response.json()
	print(data)
	#print(data[0]['name'])
	return render(request, rootDir+'index.html')

def dashboard(request):
	''' User dashboard page with links to all pages associated with viewing/editing their account'''
	user = request.user
	uId = user.id
	print(uId)
	return render(request, rootDir+"dashboard.html")


def prefPage(request):
	''' Dashboard link to edit user health metrics (diet/intolerances) '''
	user = request.user
	uId = user.id
	profile = Profile.objects.get(user=uId)
	form = UserPref(request.POST or None,instance=profile) 
	if form.is_valid():
		instance = form.save()
		#ßinstance.user = request.user
		instance.save() 
		return redirect(reverse("dashboard"))
	context = { 
		"form":form
		}
	return render(request, rootDir+"prefs.html",context=context)



def register(request):
    ''' Page for new user account creation and subsequent verification/redirect logic'''
    if request.method == "GET":
        return render(
            request, rootDir+"register.html",
            {"form": RegisterForm}
        )
    elif request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            newProfile = Profile.objects.create(user = user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            

            return redirect(reverse("dashboard"))
        else:
        	return HttpResponse("Form failed to validate (usually indicitve of invalid password)...make a proper redirect")


def search(request):
  ''' Recipe search page (via list of ingredients + optional advanced query paramaters such as by cuisine)'''
  return render(request, rootDir+'search.html')


def recipeList(request):
	''' List of recipe search results: includes recipe name, image, and clicable overview link'''
	response = None
	querystring = {}
	queryLength = request.GET["queryLength"]
	queryTags = request.GET["tags"]
	country = request.GET["cousineCountry"]

	querystring["number"] = queryLength
	querystring["tags"] = queryTags

	

	cs = ComplexSearch("search")

	
	if request.user.is_authenticated:
		user = request.user
		uId = user.id
		profile = Profile.objects.get(user=uId)
		cs.diet = profile.diet
		cs.intolerances = profile.intolerances

	
	if request.GET.get('ingredients'):
	

		find = "/recipes/findByIngredients"
		
		ingredients = request.GET["ingredients"]

		querystring["ingredients"] = ingredients

		ingredients = re.split(', |_|-|!.', ingredients)


		cs.includeIngredients = ingredients
		cs.number = queryLength
		cs.cuisine = country
		cs.type = queryTags
	
		searchKwgs = cs.search()
		response = api.search_recipes_complex(**searchKwgs)
		res = response.json()
		
		dataContext = res
	

	#Case 2: nothing submitted
	else:
		cs.cuisine = country
		cs.type = queryTags


		#cs.includeIngredients = ["apple","flour"]
		searchKwgs = cs.search()
		response = api.search_recipes_complex(**searchKwgs)
		res = response.json()

		
		dataContext = res
		print("you submitted nothing!")

		print(dataContext)
		print("ahhhh")

	return render(request, rootDir+'recipes.html',context=dataContext)


def recipeOverview(request,recipeId):
	''' Detailed overview of recipe, including overall cooking time, instructions, health metrics, and ingredients/cookware used '''
	recipe_id = recipeId

	testArgs = {'id': recipe_id, 'includeNutrition': False}
	propArgs = {'id':recipe_id}
	response = api.get_recipe_information(**propArgs)
	recipe_info = response.json()


	querystring = {"defaultCss":"true", "showBacklink":"false"}


	inregdientsWidget =  api.ingredientWidget(**propArgs)
	recipe_info['inregdientsWidget'] = inregdientsWidget.text

	equipmentWidget =  api.equipmentWidget(**propArgs)
	recipe_info['equipmentWidget'] = equipmentWidget.text

	nutritionWidget = api.visualize_recipe_nutrition_by_id(**propArgs)
	recipe_info['nutritionWidget'] = nutritionWidget.text

	priceWidget = api.priceWidget(**propArgs)
	priceMet = priceWidget.text
	recipe_info['priceeWidget'] = priceMet


	recipeObj = Recipe()

	recipe = recipe_info


	contextRecipe = {"recipe":recipe}



	return render(request, rootDir+'recipe.html', context=contextRecipe)

def userRecipeList(request):
	''' List of recipes saved by user; quivalant to recipe list except it includes a "remove recipe" widget '''
	user = request.user
	uId = user.id	
	profile = Profile.objects.get(user=uId)
	myRecipes = profile.saved_recipes.all()
	rList =[]
	for i in range(len(myRecipes)):
		rId = myRecipes[i].r_ID
		rName = myRecipes[i].name

		recipe = {"id":rId, "name":rName}

		
		rList.append(recipe)

	dataContext = {"recipes":rList}


	return render(request, rootDir+'userRecipes.html',context=dataContext)




def removeRecipe(request,recipeId):
	''' Removes user saved recipe '''
	user = request.user
	uId = user.id
	profile = Profile.objects.get(user=uId)
	recipeObj = dbRecipe.objects.get(r_ID=recipeId)
	profile.saved_recipes.remove(recipeObj)
	return redirect(reverse("dashboard"))


def addRecipe(request,recipeId,recipeName):
	''' adds recipe to entire database/users favorites  '''
	user = request.user
	uId = user.id
	exists = dbRecipe.objects.filter(r_ID = recipeId, name = recipeName).exists()
	

	if exists == False:
		newRecipe = dbRecipe.objects.create(r_ID = recipeId, name = recipeName)

	else:
		newRecipe = dbRecipe.objects.get(r_ID = recipeId, name = recipeName)
	

	if uId != None:
		profile = Profile.objects.get(user=uId)
		profile.saved_recipes.add(newRecipe)


	return redirect(reverse("dashboard"))



def ingredientOverview(request,ingredientId,amount=None,unit=None):
	''' Overview page of a single ingredient ''' 
	propArgs = {'id':ingredientId,'amount':amount, 'unit':unit}
	args  = {'id':ingredientId}
	response = api.get_food_information(**propArgs)
	ingredient_info = response.json()

	print(ingredient_info)

	nutrition = api.singleIngredientWidget(**args)
	ingredient_info['nutrition'] = nutrition.text

	subs = api.get_ingredient_substitutes_by_id(**args)
	subsub = subs.json()

	ingredient_info['subs'] = subsub['substitutes']

	#recipe_info = requests.get(url + recipe_info_endpoint, headers=recipe_headers).json()
	#recipe = recipe_info.json()

	querystring = {"defaultCss":"true", "showBacklink":"false"}
	ingContext = {"ingredient":ingredient_info} 
	return render(request, rootDir+"spoonacular/data/ingredient.html",context=ingContext)

def advancedQuery(request):
	''' Advanced query test page (tests live autocomplete features) '''
	return render(request, rootDir+'advancedSearch.html')

def autocompleteIngredient(request):
    ''' Live AJAX requests to Spoonacular API endpoint to autocomplete a user's input to a Spoonacular ingredient'''
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        print('ajax term ' + q)
        response = api.autocomplete_ingredient_search(query = q, number = 5)
        result = response.json()
        results = []
        for key in result:
        	results.append(key['name'])
        data = json.dumps(results)

    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def autocompleteRecipe(request):
    ''' Live AJAX request to autocomplete Spoonacular recipes saved to local Django database '''
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        print('ajax term ' + q)
        search_qs = dbRecipe.objects.filter(name__startswith=q)
        results = []
        print(q)

        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

#NOTE THE FOLLOWING VIEW ARE FUTURE, NO FULLY IMPLEMENTED FEATURES  

def mealPlan(request):
    return render(request, rootDir+"mealPlan.html")

def shoppingList(request):
    return render(request, rootDir+"shoppingList.html")

def socialLogin(request):
    ''' Allows for account creation/login via external social media sites such as google, facebook, ect. '''
    return render(request, rootDir+"socialLogin.html")

def spoonacularEndpoints(request):
    return render(request, rootDir+"spoonacular/apiEndpoints.html")

def fitbitPage(request):
	''' Currently unimplimented means of interacting with one's Fitbit metrics '''
	
	return render(request, rootDir+"fitbitPage.html")

