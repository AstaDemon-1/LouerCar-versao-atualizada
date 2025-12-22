from rest_framework import serializers
from user.models import Usuario, PerfilCliente, Tag, Grupo
from carro.models import Carro
from aluguel.models import Aluguel, SolicitacaoAluguel, Pagamento


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id_tag', 'nome', 'cor', 'icone', 'descricao']


class UsuarioSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'username', 'email', 'is_active', 'is_staff', 
                  'is_superuser', 'foto_perfil', 'data_cadastro', 'tags']


class PerfilClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = PerfilCliente
        fields = ['id_perfil_cliente', 'usuario', 'CNH', 'telefone', 
                  'endereco', 'criado_em', 'atualizado_em']


class CarroSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Carro
        fields = ['id_carro', 'modelo', 'placa', 'ano', 'status', 'status_display',
                  'preco_diaria', 'foto_url', 'descricao', 'criado_em']


class AluguelSerializer(serializers.ModelSerializer):
    carro = CarroSerializer(read_only=True)
    perfil_cliente = PerfilClienteSerializer(read_only=True)
    funcionario = UsuarioSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Aluguel
        fields = ['id_aluguel', 'carro', 'perfil_cliente', 'funcionario',
                  'data_inicio', 'data_fim', 'valor', 'status', 'status_display']


class SolicitacaoAluguelSerializer(serializers.ModelSerializer):
    carro = CarroSerializer(read_only=True)
    perfil_cliente = PerfilClienteSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = SolicitacaoAluguel
        fields = ['id_solicitacao', 'carro', 'perfil_cliente', 
                  'data_inicio', 'data_fim', 'valor_estimado', 
                  'status', 'status_display', 'observacoes', 'criado_em']


class PagamentoSerializer(serializers.ModelSerializer):
    aluguel = AluguelSerializer(read_only=True)
    metodo_display = serializers.CharField(source='get_metodo_pagamento_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Pagamento
        fields = ['id_pagamento', 'aluguel', 'metodo_pagamento', 'metodo_display',
                  'valor', 'status', 'status_display', 'data_vencimento', 'data_pagamento']


class GrupoSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)
    
    class Meta:
        model = Grupo
        fields = ['id_grupo', 'nome', 'descricao', 'tag', 'link_whatsapp']