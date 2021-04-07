from django.shortcuts import render, redirect
from CapstoneWebApp.forms import RegisterForm
from django.contrib.auth import login
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse

import requests



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
    return render(request, rootDir+'index.html')


def test(request):




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

            login(request, user)

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


	return render(request, rootDir+'recipe.html', context=contextRecipe)
