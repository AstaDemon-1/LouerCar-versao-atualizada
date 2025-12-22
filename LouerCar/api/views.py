from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import Usuario, PerfilCliente, Tag, Grupo
from carro.models import Carro
from aluguel.models import Aluguel, SolicitacaoAluguel, Pagamento

from .serializers import (
    UsuarioSerializer, PerfilClienteSerializer, TagSerializer, 
    GrupoSerializer, CarroSerializer, AluguelSerializer,
    SolicitacaoAluguelSerializer, PagamentoSerializer
)


class CarroViewSet(viewsets.ModelViewSet):
    """API para Carros"""
    queryset = Carro.objects.all()
    serializer_class = CarroSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        """Lista apenas carros disponíveis"""
        carros = Carro.objects.filter(status='disponivel')
        serializer = self.get_serializer(carros, many=True)
        return Response(serializer.data)


class AluguelViewSet(viewsets.ModelViewSet):
    """API para Aluguéis"""
    serializer_class = AluguelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Clientes veem apenas seus aluguéis"""
        user = self.request.user
        if user.is_staff:
            return Aluguel.objects.all()
        else:
            try:
                perfil = PerfilCliente.objects.get(usuario=user)
                return Aluguel.objects.filter(perfil_cliente=perfil)
            except PerfilCliente.DoesNotExist:
                return Aluguel.objects.none()


class SolicitacaoAluguelViewSet(viewsets.ModelViewSet):
    """API para Solicitações"""
    serializer_class = SolicitacaoAluguelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Clientes veem apenas suas solicitações"""
        user = self.request.user
        if user.is_staff:
            return SolicitacaoAluguel.objects.all()
        else:
            try:
                perfil = PerfilCliente.objects.get(usuario=user)
                return SolicitacaoAluguel.objects.filter(perfil_cliente=perfil)
            except PerfilCliente.DoesNotExist:
                return SolicitacaoAluguel.objects.none()
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Lista solicitações pendentes (apenas staff)"""
        if not request.user.is_staff:
            return Response({'error': 'Apenas funcionários'}, status=403)
        
        solicitacoes = SolicitacaoAluguel.objects.filter(status='pendente')
        serializer = self.get_serializer(solicitacoes, many=True)
        return Response(serializer.data)


class PagamentoViewSet(viewsets.ReadOnlyModelViewSet):
    """API para Pagamentos (apenas leitura)"""
    serializer_class = PagamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Clientes veem apenas seus pagamentos"""
        user = self.request.user
        if user.is_staff:
            return Pagamento.objects.all()
        else:
            try:
                perfil = PerfilCliente.objects.get(usuario=user)
                return Pagamento.objects.filter(aluguel__perfil_cliente=perfil)
            except PerfilCliente.DoesNotExist:
                return Pagamento.objects.none()


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """API para Usuários (apenas admin)"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Retorna dados do usuário logado"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """API para Tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class GrupoViewSet(viewsets.ReadOnlyModelViewSet):
    """API para Grupos"""
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [permissions.IsAuthenticated]