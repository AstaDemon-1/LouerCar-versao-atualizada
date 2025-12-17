from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ⭐ A home agora vem do user.urls ⭐
    path('', include('user.urls')),  
    path('', include('carro.urls')),
    path('', include('aluguel.urls')),
]