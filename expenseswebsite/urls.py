
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('expenses.urls')),
    path('authentication/', include('authenticationapp.urls')), 
    path('admin/', admin.site.urls),
    
] 
