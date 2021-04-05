
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
	time = models.TimeField()

	def __str__(self):
		return str(self.name)

#Despite primary keys being automatically defined, theyre manually defined here since thyere equivalant to Spoonacular's api
class Ingredient(models.Model):
	i_ID = models.IntegerField(max_length=6, primary_key=True)
	name = models.CharField(max_length=128)
	price = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=6)
	recipes = models.ManyToManyField(Recipe)


#TODO make this dissapear with a depenacy relationship (althoug this is sucesfully linking all use cases I can think of)
class QuantityPerRecipe(models.Model):
	recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
	quantity = models.IntegerField()





#TODO add a "In My Fridge" feature. Will help with meal plans

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)

    #need to  consider different countries/ metrics
    weight = models.DecimalField(null = True, blank = True,decimal_places=2,max_digits=6)
    height = models.DecimalField(null = True, blank = True,decimal_places=2,max_digits=3)

    saved_recipes = models.ManyToManyField(Recipe)

    def __str__(self):
    	return(self.user.username + "; First Name: " + self.user.first_name)



class FridgeItem(models.Model):
	#consider potentially saving a meal itself in the fridge
	ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
	owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
	quantity = models.IntegerField(max_length=4)
	

	purchaseDate = models.DateTimeField(null = True, blank = True)
