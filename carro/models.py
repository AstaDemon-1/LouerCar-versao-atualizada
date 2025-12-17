from django.db import models

class Carro(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('manutencao', 'Manutenção'),
    ]
    
    id_carro = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10, unique=True)
    ano = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    
    # ⭐ CAMPOS OBRIGATÓRIOS ⭐
    preco_diaria = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=150.00,
        help_text='Preço do aluguel por dia'
    )
    foto_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='URL da foto do carro (ex: Unsplash, Pexels)'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        help_text='Descrição detalhada do carro (motor, câmbio, etc)'
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carro'
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.modelo} - {self.placa}"
    
    def esta_disponivel(self):
        """Verifica se o carro está disponível para aluguel"""
        return self.status == 'disponivel'
    
    def get_status_badge(self):
        """Retorna a classe CSS do badge de acordo com o status"""
        badges = {
            'disponivel': 'bg-success',
            'alugado': 'bg-warning',
            'manutencao': 'bg-danger',
        }
        return badges.get(self.status, 'bg-secondary')
    
    def get_foto_url(self):
        """Retorna URL da foto ou None"""
        if self.foto_url:
            return self.foto_url
        # Se não tiver foto, retorna None (template mostra ícone)
        return None