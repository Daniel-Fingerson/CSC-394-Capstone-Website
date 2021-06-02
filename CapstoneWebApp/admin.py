from django.contrib import admin
from CapstoneWebApp.models import Recipe,Ingredient,Profile, Diet, Intolerance


# Registers models so that they can be manually edited via Django's built in admin page
# Note that this page is only acessible after manually creating an admin user (via command line utility manage.py)
# 	Ex: $python manage.py createsuperuser


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