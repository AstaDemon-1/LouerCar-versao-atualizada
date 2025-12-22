from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),  
    path('', include('carro.urls')),
    path('', include('aluguel.urls')),
    
    # API REST
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]