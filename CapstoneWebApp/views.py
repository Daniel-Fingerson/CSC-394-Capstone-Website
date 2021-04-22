from django.shortcuts import render, redirect
from CapstoneWebApp.forms import RegisterForm
from django.contrib.auth import login
from django.urls import reverse

from bootstrap_modal_forms.generic import BSModalCreateView

from CapstoneWebApp.models import Profile
from CapstoneWebApp.models import Recipe as dbRecipe


import fitbit
import CapstoneWebApp.gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime

# Create your views here.
from django.http import HttpResponse

import requests
import spoonacular as sp
api = sp.API("e49afb82519a407db4b10de35ddf7252")



class Recipe:
	def __init__(self):
		self.title = "idk"
#TODO make this dynamicly generated (or saved in a static dir/in settings)
rootDir = "CSC-394-Capstone-Website/"
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
headers = {
		  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
		  'x-rapidapi-key': "2bd3ea57damsh9a529e22e7b79eep1af36ejsne5a774d5e4d6",
		  }

def index(request):
	#return HttpResponse("Hello CSC394 Blue Group. You're at the group's index page .")
	print("ahh")
	if request.method == "GET":
		print("its a get request")
	elif request.method == "POST":
		print("its a post request (most likely an Ouath redriect )")
	return render(request, rootDir+'index.html')


def test(request):
	response = api.parse_ingredients("3.5 cups King Arthur flour", servings=1)
	data = response.json()
	print(data)
	#print(data[0]['name'])
	return render(request, rootDir+'index.html')

def dashboard(request):
    return render(request, rootDir+"dashboard.html")

def register(request):
    if request.method == "GET":
        return render(
            request, rootDir+"register.html",
            {"form": RegisterForm}
        )
    elif request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect(reverse("dashboard"))
        else:
        	return HttpResponse("Form failed to validate (usually indicitve of invalid password)...make a proper redirect")


def search(request):
  return render(request, rootDir+'search.html')

#@app.route('/recipes')
def recipeList(request):

	response = None
	querystring = {}
	queryLength = request.GET["queryLength"]
	queryTags = request.GET["tags"]

	querystring["number"] = queryLength
	querystring["tags"] = queryTags



	if request.GET.get('ingredients'):
		print("you did it!")

		#TODO REMOVE IMEDIETLY!!!

		find = "/recipes/findByIngredients"
		#find = "/recipes/random"



		#querystring = {"ingredients":"beef,flour,sugar","number":"5","ranking":"1","ignorePantry":"true"}

		ingredients = request.GET["ingredients"]



		querystring["ingredients"] = ingredients

		querystring["tags"] = "vegan"


		print(ingredients)



		response = requests.get((url+find), headers=headers, params = querystring)
		data = response.json()
		print("here it is")
		print(data)

		dataContext = {"recipes": data}
		dataContext["specialParam"] =  "Number of results shown: " + str(queryLength)
		dataContext["ingredients"] =  ingredients

		#print(data)
		#print('that was a dict')
		#print(data)
		#print(len(data))

	#Case 2: nothing submitted
	else:

		find = "/recipes/random"
		querystring["specialParam"] = "Randomly Generated"
		response = requests.get((url+find), headers=headers, params = querystring)
		data = response.json()
		dataContext = data
		dataContext["specialParam"] = "(Randomly Generated) " + "Number of results shown: " + str(queryLength)
		print("you submitted nothing!")

		print(dataContext)
		print("ahhhh")

	return render(request, rootDir+'recipes.html',context=dataContext)

def userRecipeList(request):
	user = request.user
	uId = user.id
	print(user)
	print(uId)
	profile = Profile.objects.get(user=uId)
	print(profile)
	myRecipes = profile.saved_recipes.all()
	rList =[]
	for i in range(len(myRecipes)):
		rId = myRecipes[i].r_ID
		rName = myRecipes[i].name
		
		#dataContext = [entry for entry in myRecipes]
		#print(dataContext)

		recipe = {"id":rId, "name":rName}

		
		rList.append(recipe)
	#rList.append(recipe)

	dataContext = {"recipes":rList}


	return render(request, rootDir+'userRecipes.html',context=dataContext)

def dashboard(request):
	user = request.user
	uId = user.id
	print(uId)
	return render(request, rootDir+"dashboard.html")

def socialLogin(request):
    return render(request, rootDir+"socialLogin.html")


def fitbitPage(request):
	'''
	CLIENT_ID="22CDBH"
	CLIENT_SECRET="6dd214dc3a8a395ca629e5106c23dc92"
	ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
	REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
	auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
	'''
	#unauth_client = fitbit.Fitbit('22CDBH', '6dd214dc3a8a395ca629e5106c23dc92',access_token='d8d36c86af31471d1487f1f7044eebde93e5f31e')
	#unauth_client.food_units()
	return render(request, rootDir+"fitbitPage.html")

def register(request):
    if request.method == "GET":
        return render(
            request, rootDir+"register.html",
            {"form": RegisterForm}
        )
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return redirect(reverse("dashboard"))
        else:
        	return HttpResponse("Form failed to validate (usually indicitve of invalid password)...make a proper redirect")

#Detailed overview of recipe
def recipeOverview(request,recipeId):
	#recipe_id = request.args['id']
	recipe_id = recipeId


	recipe_info_endpoint = "/recipes/{0}/information".format(recipe_id)
	ingedientsWidget = "/recipes/{0}/ingredientWidget".format(recipe_id)
	equipmentWidget = "/recipes/{0}/equipmentWidget".format(recipe_id)
	recipe_headers = {
		  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
		  'x-rapidapi-key': "2bd3ea57damsh9a529e22e7b79eep1af36ejsne5a774d5e4d6",
		  }
	recipe_info = requests.get(url + recipe_info_endpoint, headers=recipe_headers).json()
	#recipe = recipe_info.json()

	querystring = {"defaultCss":"true", "showBacklink":"false"}

	recipe_info['inregdientsWidget'] = requests.get(url + ingedientsWidget, headers=recipe_headers, params=querystring).text
	recipe_info['equipmentWidget'] = requests.get(url + equipmentWidget, headers=recipe_headers, params=querystring).text

	ingredients = requests.get(url + ingedientsWidget, headers=recipe_headers)

	#ingredientInfo = ingredients.json()




	#recipe["title"] = "test"

	recipeObj = Recipe()

	recipe = recipe_info

	#recipe['ingridients'] = ingredients

	#print(recipe)

	#print(recipe['title'])

	print(ingredients.text)





	contextRecipe = {"recipe":recipe}

	#print(contextRecipe)


	return render(request, rootDir+'recipe.html', context=contextRecipe)

#removes user saved recipe
def removeRecipe(request,recipeId):
	user = request.user
	uId = user.id
	profile = Profile.objects.get(user=uId)
	recipeObj = dbRecipe.objects.get(r_ID=recipeId)
	profile.saved_recipes.remove(recipeObj)
	return redirect(reverse("dashboard"))

#adds recipe to entire database/users favorites
#TODO dont add if allrady present in their favorires/ dont readd to aggregate databse if already present 
def addRecipe(request,recipeId,recipeName):
	user = request.user
	uId = user.id
	exists = dbRecipe.objects.get(r_ID = recipeId)
	if exists:
		newRecipe = exists
	else:
		newRecipe = dbRecipe.objects.create(r_ID = recipeId, name = recipeName)

	if uId != None:
		profile = Profile.objects.get(user=uId)
		profile.saved_recipes.add(newRecipe)


	return redirect(reverse("dashboard"))
	