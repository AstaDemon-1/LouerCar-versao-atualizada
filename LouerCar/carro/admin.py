from django.contrib import admin
from .models import Carro

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ('id_carro', 'modelo', 'placa', 'ano', 'status', 'criado_em')
    list_filter = ('status', 'ano', 'criado_em')
    search_fields = ('modelo', 'placa')
    readonly_fields = ('criado_em', 'atualizado_em')
    ordering = ('-criado_em',)
    
    fieldsets = (
        ('Informações do Carro', {
            'fields': ('modelo', 'placa', 'ano')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Torna a placa readonly após criação"""
        if obj:  # Editando
            return self.readonly_fields + ('placa',)
        return self.readonly_fields