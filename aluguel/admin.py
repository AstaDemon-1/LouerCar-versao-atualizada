from django.contrib import admin
from .models import Aluguel

@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):
    list_display = (
        'id_aluguel', 
        'carro', 
        'perfil_cliente', 
        'funcionario', 
        'data_inicio', 
        'data_fim', 
        'valor', 
        'status',
        'criado_em'
    )
    list_filter = ('status', 'data_inicio', 'data_fim', 'criado_em')
    search_fields = (
        'carro__modelo', 
        'carro__placa', 
        'perfil_cliente__usuario__username',
        'perfil_cliente__CNH',
        'funcionario__username'
    )
    readonly_fields = ('criado_em', 'atualizado_em')
    ordering = ('-criado_em',)
    date_hierarchy = 'data_inicio'
    
    fieldsets = (
        ('Informações do Aluguel', {
            'fields': ('perfil_cliente', 'carro', 'funcionario')
        }),
        ('Período', {
            'fields': ('data_inicio', 'data_fim')
        }),
        ('Valores e Status', {
            'fields': ('valor', 'status')
        }),
        ('Datas de Sistema', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Torna alguns campos readonly após criação"""
        if obj:  # Editando
            return self.readonly_fields + ('carro', 'perfil_cliente')
        return self.readonly_fields