# ADICIONE ESTE MODELO NO FINAL DO ARQUIVO aluguel/models.py

from django.db import models
from user.models import PerfilCliente, Usuario
from carro.models import Carro
from django.core.mail import send_mail
from django.conf import settings

class Pagamento(models.Model):
    """
    Modelo para gerenciar pagamentos de aluguéis aprovados
    """
    METODO_CHOICES = [
        ('pix', 'PIX'),
        ('cartao', 'Cartão de Crédito'),
        ('boleto', 'Boleto Bancário'),
        ('dinheiro', 'Dinheiro'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Aguardando Pagamento'),
        ('processando', 'Processando'),
        ('aprovado', 'Pago'),
        ('recusado', 'Recusado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id_pagamento = models.AutoField(primary_key=True)
    aluguel = models.OneToOneField(
        'Aluguel',
        on_delete=models.CASCADE,
        related_name='pagamento'
    )
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=METODO_CHOICES,
        default='pix'
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )
    data_vencimento = models.DateTimeField()
    data_pagamento = models.DateTimeField(null=True, blank=True)
    
    # Dados para PIX
    chave_pix = models.CharField(max_length=255, blank=True, null=True)
    qr_code_pix = models.TextField(blank=True, null=True)
    
    # Dados para Boleto
    codigo_barras = models.CharField(max_length=255, blank=True, null=True)
    linha_digitavel = models.CharField(max_length=255, blank=True, null=True)
    
    # Controle
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pagamento'
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Pagamento #{self.id_pagamento} - Aluguel #{self.aluguel.id_aluguel}"
    
    def get_status_badge(self):
        """Retorna a classe CSS do badge"""
        badges = {
            'pendente': 'bg-warning',
            'processando': 'bg-info',
            'aprovado': 'bg-success',
            'recusado': 'bg-danger',
            'cancelado': 'bg-secondary',
        }
        return badges.get(self.status, 'bg-secondary')
    
    def enviar_email_pagamento_pendente(self):
        """Envia email notificando sobre pagamento pendente"""
        cliente = self.aluguel.perfil_cliente.usuario
        
        subject = f'🚗 Pagamento Pendente - Aluguel #{self.aluguel.id_aluguel}'
        message = f"""
        Olá {cliente.username}!
        
        Sua solicitação de aluguel foi APROVADA! 🎉
        
        Detalhes do Aluguel:
        - Carro: {self.aluguel.carro.modelo} ({self.aluguel.carro.placa})
        - Período: {self.aluguel.data_inicio.strftime('%d/%m/%Y')} até {self.aluguel.data_fim.strftime('%d/%m/%Y')}
        - Valor: R$ {self.valor}
        
        Método de Pagamento: {self.get_metodo_pagamento_display()}
        Status: {self.get_status_display()}
        Vencimento: {self.data_vencimento.strftime('%d/%m/%Y %H:%M')}
        
        Acesse o sistema para ver os detalhes do pagamento:
        {settings.SITE_URL}/minhas-solicitacoes/
        
        Atenciosamente,
        Equipe LouerCar
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [cliente.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
    
    def enviar_email_pagamento_aprovado(self):
        """Envia email notificando pagamento aprovado"""
        cliente = self.aluguel.perfil_cliente.usuario
        
        subject = f'✅ Pagamento Confirmado - Aluguel #{self.aluguel.id_aluguel}'
        message = f"""
        Olá {cliente.username}!
        
        Seu pagamento foi CONFIRMADO! ✅
        
        Detalhes do Aluguel:
        - Carro: {self.aluguel.carro.modelo} ({self.aluguel.carro.placa})
        - Período: {self.aluguel.data_inicio.strftime('%d/%m/%Y')} até {self.aluguel.data_fim.strftime('%d/%m/%Y')}
        - Valor Pago: R$ {self.valor}
        - Data do Pagamento: {self.data_pagamento.strftime('%d/%m/%Y %H:%M') if self.data_pagamento else 'N/A'}
        
        Seu carro estará pronto para retirada na data combinada!
        
        Atenciosamente,
        Equipe LouerCar
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [cliente.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erro ao enviar email: {e}")


class SolicitacaoAluguel(models.Model):
    """
    Modelo para SOLICITAÇÕES de aluguel feitas pelos clientes.
    Funcionários aprovam e transformam em Aluguel oficial.
    """
    STATUS_CHOICES = [
        ('pendente', 'Aguardando Aprovação'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('cancelado', 'Cancelado pelo Cliente'),
    ]
    
    id_solicitacao = models.AutoField(primary_key=True)
    perfil_cliente = models.ForeignKey(
        PerfilCliente,
        on_delete=models.CASCADE,
        db_column='perfil_cliente_id',
        related_name='solicitacoes'
    )
    carro = models.ForeignKey(
        Carro,
        on_delete=models.CASCADE,
        db_column='carro_id',
        related_name='solicitacoes'
    )
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True, null=True, help_text='Observações do cliente')
    
    # Datas de controle
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    # Quando aprovado, armazena o aluguel criado
    aluguel_criado = models.OneToOneField(
        'Aluguel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitacao_origem'
    )
    
    class Meta:
        db_table = 'solicitacao_aluguel'
        verbose_name = 'Solicitação de Aluguel'
        verbose_name_plural = 'Solicitações de Aluguel'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Solicitação #{self.id_solicitacao} - {self.perfil_cliente.usuario.username}"
    
    def get_status_badge(self):
        """Retorna a classe CSS do badge"""
        badges = {
            'pendente': 'bg-warning',
            'aprovado': 'bg-success',
            'rejeitado': 'bg-danger',
            'cancelado': 'bg-secondary',
        }
        return badges.get(self.status, 'bg-secondary')
    
    def calcular_dias(self):
        """Calcula quantos dias de aluguel"""
        if self.data_fim and self.data_inicio:
            duracao = self.data_fim - self.data_inicio
            return max(1, duracao.days)
        return 0
    
    def tem_pagamento_pendente(self):
        """Verifica se há pagamento pendente"""
        if self.aluguel_criado and hasattr(self.aluguel_criado, 'pagamento'):
            return self.aluguel_criado.pagamento.status == 'pendente'
        return False


class Aluguel(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id_aluguel = models.AutoField(primary_key=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    # Relacionamentos
    perfil_cliente = models.ForeignKey(
        PerfilCliente, 
        on_delete=models.CASCADE, 
        db_column='perfil_cliente_id_perfil_cliente',
        related_name='alugueis'
    )
    carro = models.ForeignKey(
        Carro, 
        on_delete=models.CASCADE, 
        db_column='carro_id_carro',
        related_name='alugueis'
    )
    funcionario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        db_column='id_funcionario',
        related_name='alugueis_gerenciados',
        limit_choices_to={'is_staff': True}
    )
    
    class Meta:
        db_table = 'aluguel'
        verbose_name = 'Aluguel'
        verbose_name_plural = 'Aluguéis'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Aluguel #{self.id_aluguel} - {self.carro.modelo} ({self.get_status_display()})"
    
    def get_status_badge(self):
        """Retorna a classe CSS do badge de acordo com o status"""
        badges = {
            'ativo': 'bg-info',
            'finalizado': 'bg-success',
            'cancelado': 'bg-secondary',
        }
        return badges.get(self.status, 'bg-secondary')
    
    def calcular_duracao(self):
        """Calcula a duração do aluguel em dias"""
        if self.data_fim and self.data_inicio:
            duracao = self.data_fim - self.data_inicio
            return duracao.days
        return 0
    
    def esta_ativo(self):
        """Verifica se o aluguel está ativo"""
        return self.status == 'ativo'
    
    def tem_pagamento(self):
        """Verifica se tem pagamento associado"""
        return hasattr(self, 'pagamento')
    
    def save(self, *args, **kwargs):
        """Atualiza o status do carro ao salvar o aluguel"""
        if self.status == 'ativo' and self.carro.status != 'alugado':
            self.carro.status = 'alugado'
            self.carro.save()
        
        if self.status in ['finalizado', 'cancelado']:
            outros_ativos = Aluguel.objects.filter(
                carro=self.carro, 
                status='ativo'
            ).exclude(id_aluguel=self.pk).exists()
            
            if not outros_ativos:
                self.carro.status = 'disponivel'
                self.carro.save()
        
        super().save(*args, **kwargs)