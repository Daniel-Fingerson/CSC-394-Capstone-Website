from django.contrib import admin
from django.urls import include, path
from schema_graph.views import Schema



urlpatterns = [
    path('', include('CapstoneWebApp.urls')),
    
    path('admin/', admin.site.urls),
    path("schema/", Schema.as_view()),

    
]