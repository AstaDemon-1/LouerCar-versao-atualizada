from django.urls import path
from . import views

urlpatterns = [
    # URLs de Carro
    path('carros/', views.carro_list, name='carro_list'),
    path('carros/criar/', views.carro_create, name='carro_create'),
    path('carros/<int:pk>/', views.carro_detail, name='carro_detail'),
    path('carros/<int:pk>/editar/', views.carro_update, name='carro_update'),
    path('carros/<int:pk>/deletar/', views.carro_delete, name='carro_delete'),
    path('carros/<int:pk>/status/', views.carro_change_status, name='carro_change_status'),
]