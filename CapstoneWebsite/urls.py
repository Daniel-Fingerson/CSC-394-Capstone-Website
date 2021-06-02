from django.contrib import admin
from django.urls import include, path
from schema_graph.views import Schema

#Multiple apps can be present within a Django project
#This project only contains one, so this links that, as well as a Django admin page, to itself

#An overview of the projects' schema via a PyPi project is also imported/accessible here

urlpatterns = [
    path('', include('CapstoneWebApp.urls')),
    
    path('admin/', admin.site.urls),
    path("schema/", Schema.as_view()),

    
]