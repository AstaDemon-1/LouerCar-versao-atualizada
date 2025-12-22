from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'carros', views.CarroViewSet, basename='carro')
router.register(r'alugueis', views.AluguelViewSet, basename='aluguel')
router.register(r'solicitacoes', views.SolicitacaoAluguelViewSet, basename='solicitacao')
router.register(r'pagamentos', views.PagamentoViewSet, basename='pagamento')
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'grupos', views.GrupoViewSet, basename='grupo')

urlpatterns = [
    path('', include(router.urls)),
]