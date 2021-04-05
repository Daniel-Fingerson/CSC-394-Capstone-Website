from django.contrib import admin
from CapstoneWebApp.models import Recipe,Ingredient,FridgeItem,Profile


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
	
	pass
    

class IngredientAdmin(admin.ModelAdmin):
	
	pass

class FridgeItemAdmin(admin.ModelAdmin):
	
	pass
    

class ProfileAdmin(admin.ModelAdmin):
	
	pass

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FridgeItem, FridgeItemAdmin)
admin.site.register(Profile, ProfileAdmin)