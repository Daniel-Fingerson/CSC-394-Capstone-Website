from django.contrib import admin
from CapstoneWebApp.models import Recipe,Ingredient,Profile, Diet, Intolerance


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
	pass
    
class IngredientAdmin(admin.ModelAdmin):	
	pass
  
class ProfileAdmin(admin.ModelAdmin):
	pass



class DietAdmin(admin.ModelAdmin):	
	pass
  
class IntoleranceAdmin(admin.ModelAdmin):
	pass



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Diet, DietAdmin)
admin.site.register(Intolerance, IntoleranceAdmin)