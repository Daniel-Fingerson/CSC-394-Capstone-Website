
from django.db import models
from django.contrib.auth.models import User

'''
Source document for defining models stored in Django's model API

Each class is mapped to a corresponding SQL table
Each object instance is mapped to a corresponding SQL entry
Each instance is accesible via the API, most often through 'views.py' (primary source of backend rendering)

'''

class Recipe(models.Model):
	''' Recipe ID and name used in Spoonacular queries; remaining data is rendered at runtime '''
	r_ID = models.IntegerField(max_length=6, primary_key=True)
	name = models.CharField(max_length=128)
	
	def __str__(self):
		return str(self.name)


class Ingredient(models.Model):
	''' Ingredient ID and attributes used in Spoonacular queries; currently nonfunctional (future 'User' like/dislike feature) '''
	i_ID = models.IntegerField(max_length=6, primary_key=True)
	name = models.CharField(max_length=128)
	price = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=6)
	recipes = models.ManyToManyField(Recipe)

	def __str__(self):
		return(self.name)


class Diet(models.Model):
	''' Diets defined in Spoonacular API for limiting search queries (via Profile) '''
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=1024,null=True,blank=True)


	def __str__(self):
		return(self.name)

class Intolerance(models.Model):
	''' Food intolrances defined in Spoonacular API for limiting search queries (via Profile) '''
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=1024,null=True,blank=True)

	def __str__(self):
		return(self.name)


class Profile(models.Model):
    ''' Custom class which extends usability of Django's built in 'User' functionality '''    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=30, blank=True, null = True)
    dob = models.DateField(null=True, blank=True)

    weight = models.DecimalField(null = True, blank = True,decimal_places=2,max_digits=6)
    height = models.DecimalField(null = True, blank = True,decimal_places=2,max_digits=3)

    saved_recipes = models.ManyToManyField(Recipe, blank = True, null = True,symmetrical=False)

    diet = models.ForeignKey(Diet, on_delete=models.PROTECT, blank = True, null = True)
    intolerances = models.ManyToManyField(Intolerance, blank = True, null = True)
    dislikedFoods = models.ManyToManyField(Ingredient, blank = True, null = True)

    def __str__(self):
    	return(self.user.username + " First Name: " + self.user.first_name)


