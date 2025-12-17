from django.contrib import admin
from .models import Usuario, PerfilCliente, Grupo, UsuarioGrupo

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'data_cadastro')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'data_cadastro')
    search_fields = ('username', 'email')
    readonly_fields = ('data_cadastro',)
    ordering = ('-data_cadastro',)

@admin.register(PerfilCliente)
class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = ('id_perfil_cliente', 'usuario', 'CNH', 'telefone', 'criado_em')
    list_filter = ('criado_em', 'atualizado_em')
    search_fields = ('CNH', 'telefone', 'usuario__username')
    readonly_fields = ('criado_em', 'atualizado_em')
    ordering = ('-criado_em',)

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('id_grupo', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)

@admin.register(UsuarioGrupo)
class UsuarioGrupoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'grupo')
    list_filter = ('grupo',)
    search_fields = ('usuario__username', 'grupo__nome')