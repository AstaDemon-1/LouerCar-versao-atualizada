from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # URLs de Autenticação
    path('', auth_views.home, name='home'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('cadastro/', auth_views.register, name='register'),
    path('dashboard/cliente/', auth_views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard/funcionario/', auth_views.dashboard_funcionario, name='dashboard_funcionario'),
    
    # ⭐ MEU PERFIL ⭐
    path('meu-perfil/', views.meu_perfil, name='meu_perfil'),
    path('meu-perfil/editar/', views.editar_meu_perfil, name='editar_meu_perfil'),
    
    # URLs de Usuário (APENAS ADMIN)
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/criar/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/', views.usuario_detail, name='usuario_detail'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/deletar/', views.usuario_delete, name='usuario_delete'),
    
    # URLs de Perfil Cliente (APENAS ADMIN)
    path('perfis/', views.perfil_list, name='perfil_list'),
    path('perfis/criar/', views.perfil_create, name='perfil_create'),
    path('perfis/<int:pk>/', views.perfil_detail, name='perfil_detail'),
    path('perfis/<int:pk>/editar/', views.perfil_update, name='perfil_update'),
    path('perfis/<int:pk>/deletar/', views.perfil_delete, name='perfil_delete'),
    
    # ⭐ URLs de TAG (APENAS ADMIN) - NOVO ⭐
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/criar/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/editar/', views.tag_update, name='tag_update'),
    path('tags/<int:pk>/deletar/', views.tag_delete, name='tag_delete'),
    
    # ⭐ URLs de USUÁRIO-TAG (APENAS ADMIN) - NOVO ⭐
    path('usuario-tag/adicionar/', views.usuario_tag_create, name='usuario_tag_create'),
    path('usuario-tag/<int:pk>/remover/', views.usuario_tag_delete, name='usuario_tag_delete'),
    
    # URLs de Grupo (APENAS ADMIN)
    path('grupos/', views.grupo_list, name='grupo_list'),
    path('grupos/criar/', views.grupo_create, name='grupo_create'),
    path('grupos/<int:pk>/editar/', views.grupo_update, name='grupo_update'),
    path('grupos/<int:pk>/deletar/', views.grupo_delete, name='grupo_delete'),
    
    # URLs de Usuário-Grupo (APENAS ADMIN)
    path('usuario-grupo/adicionar/', views.usuario_grupo_create, name='usuario_grupo_create'),
    path('usuario-grupo/<int:pk>/remover/', views.usuario_grupo_delete, name='usuario_grupo_delete'),
    
    # ⭐ URLs de MEUS GRUPOS (QUALQUER USUÁRIO) - NOVO ⭐
    path('meus-grupos/', views.meus_grupos, name='meus_grupos'),
    path('meus-grupos/entrar/<int:grupo_id>/', views.entrar_grupo, name='entrar_grupo'),
]