from django.urls import path
from . import views

urlpatterns = [
    # ============================================
    # URLs PARA CLIENTES (Solicitações)
    # ============================================
    path('solicitar-aluguel/', views.solicitar_aluguel, name='solicitar_aluguel'),
    path('solicitar-aluguel/<int:carro_id>/', views.solicitar_aluguel, name='solicitar_aluguel_carro'),
    path('minhas-solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'),
    path('cancelar-solicitacao/<int:pk>/', views.cancelar_solicitacao, name='cancelar_solicitacao'),
    
    # ============================================
    # URLs DE PAGAMENTO (NOVO)
    # ============================================
    path('meu-pagamento/<int:solicitacao_id>/', views.meu_pagamento, name='meu_pagamento'),
    path('pagamentos-pendentes/', views.pagamentos_pendentes, name='pagamentos_pendentes'),
    path('confirmar-pagamento/<int:pagamento_id>/', views.confirmar_pagamento, name='confirmar_pagamento'),
    
    # ============================================
    # URLs PARA FUNCIONÁRIOS (Aprovar/Rejeitar)
    # ============================================
    path('solicitacoes-pendentes/', views.solicitacoes_pendentes, name='solicitacoes_pendentes'),
    path('aprovar-solicitacao/<int:pk>/', views.aprovar_solicitacao, name='aprovar_solicitacao'),
    path('rejeitar-solicitacao/<int:pk>/', views.rejeitar_solicitacao, name='rejeitar_solicitacao'),
    
    # ============================================
    # URLs ORIGINAIS DE ALUGUEL (Funcionários)
    # ============================================
    path('alugueis/', views.aluguel_list, name='aluguel_list'),
    path('alugueis/criar/', views.aluguel_create, name='aluguel_create'),
    path('alugueis/<int:pk>/', views.aluguel_detail, name='aluguel_detail'),
    path('alugueis/<int:pk>/editar/', views.aluguel_update, name='aluguel_update'),
    path('alugueis/<int:pk>/deletar/', views.aluguel_delete, name='aluguel_delete'),
    path('alugueis/<int:pk>/status/', views.aluguel_change_status, name='aluguel_change_status'),
    path('alugueis/<int:pk>/finalizar/', views.aluguel_finalizar, name='aluguel_finalizar'),
    path('alugueis/<int:pk>/cancelar/', views.aluguel_cancelar, name='aluguel_cancelar'),
]