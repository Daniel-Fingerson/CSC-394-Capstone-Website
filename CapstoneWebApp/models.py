
#TODO consdier/ implement minimum value (and potentially a default)

from django.db import models
from django.contrib.auth.models import User

#TODO either filter releavant queries or make a better dependacy relationsip on dataset 
#to, for example, show the number of relevant ingridients for a dish

#this may all be irrelevant if the data is pulled from the web
#get others input on what would be best (certain data MUST be stored; everything could theoretically be stored, but at the cost of a giant dataset whilst an api already exist)


##saving certain relevant parts of data will lower compuational complexity/ overall runtime!!


#!!!IMPORTATN TODO BIGGEST NEXT STEP reorginzae everything along these lines
#https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024


#Quantity/description will be calculated via web call rather then stored locally
#just as images are
class Recipe(models.Model):
	r_ID = models.IntegerField(max_length=6, primary_key=True)
	name = models.CharField(max_length=128)
	
	def __str__(self):
		return str(self.name)

#Despite primary keys being automatically defined, theyre manually defined here since thyere equivalant to Spoonacular's api
class Ingredient(models.Model):
	i_ID = models.IntegerField(max_length=6, primary_key=True)
	name = models.CharField(max_length=128)
	price = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=6)
	recipes = models.ManyToManyField(Recipe)

	def __str__(self):
		return(self.name)


class Diet(models.Model):
	#d_ID = models.IntegerField(max_length=6, primary_key=True)
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=1024,null=True,blank=True)


	def __str__(self):
		return(self.name)

class Intolerance(models.Model):
	#i_ID = models.IntegerField(max_length=6, primary_key=True)
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=1024,null=True,blank=True)

	def __str__(self):
		return(self.name)


#TODO add a "In My Fridge" feature. Will help with meal plans

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=30, blank=True, null = True)
    dob = models.DateField(null=True, blank=True)

    #need to  consider different countries/ metrics
    weight = models.DecimalField(null = True, blank = True,decimal_places=2,max_digits=6)
    height = models.DecimalField(null = True, blank = True,decimal_places=2,max_digits=3)

    saved_recipes = models.ManyToManyField(Recipe, blank = True, null = True,symmetrical=False)

    diet = models.ForeignKey(Diet, on_delete=models.PROTECT, blank = True, null = True)
    intolerances = models.ManyToManyField(Intolerance, blank = True, null = True)
    dislikedFoods = models.ManyToManyField(Ingredient, blank = True, null = True)

    def __str__(self):
    	return(self.user.username + " First Name: " + self.user.first_name)


