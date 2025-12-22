from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Tag(models.Model):
    """
    Tags criadas apenas por ADMIN para categorizar grupos
    """
    COLOR_CHOICES = [
        ('primary', 'Azul'),
        ('success', 'Verde'),
        ('danger', 'Vermelho'),
        ('warning', 'Amarelo'),
        ('info', 'Ciano'),
        ('purple', 'Roxo'),
        ('pink', 'Rosa'),
        ('orange', 'Laranja'),
    ]
    
    id_tag = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    cor = models.CharField(max_length=20, choices=COLOR_CHOICES, default='primary')
    icone = models.CharField(
        max_length=50, 
        default='bi-tag',
        help_text='Ícone do Bootstrap Icons (ex: bi-star, bi-heart)'
    )
    descricao = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tag'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    def get_badge_class(self):
        """Retorna classe CSS do badge"""
        return f"bg-{self.cor}"


class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    
    # Tag do grupo
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grupos'
    )
    
    # Link do WhatsApp
    link_whatsapp = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Link do grupo no WhatsApp (ex: https://chat.whatsapp.com/...)'
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grupo'
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
    
    def __str__(self):
        return self.nome


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    foto_perfil = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='URL da foto de perfil (ex: Gravatar, Imgur)'
    )
    
    # Tags do usuário
    tags = models.ManyToManyField(
        Tag,
        through='UsuarioTag',
        related_name='usuarios',
        blank=True
    )
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        """Criptografa a senha antes de salvar"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica se a senha está correta"""
        return check_password(raw_password, self.password)
    
    def get_foto_perfil(self):
        """Retorna URL da foto ou None"""
        if self.foto_perfil:
            return self.foto_perfil
        return None
    
    def get_tags(self):
        """Retorna lista de tags do usuário"""
        return self.tags.all()
    
    def get_grupos_visiveis(self):
        """Retorna grupos que o usuário pode ver baseado em suas tags"""
        tags_usuario = self.tags.all()
        
        if tags_usuario.exists():
            # Retorna grupos que têm alguma das tags do usuário
            return Grupo.objects.filter(tag__in=tags_usuario).distinct()
        else:
            # Se não tem tags, não vê nenhum grupo
            return Grupo.objects.none()


class UsuarioTag(models.Model):
    """
    Relacionamento entre Usuário e Tag
    Apenas ADMIN pode atribuir tags
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='usuario_id'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        db_column='tag_id'
    )
    atribuido_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'usuario_tag'
        unique_together = ('usuario', 'tag')
        verbose_name = 'Usuário-Tag'
        verbose_name_plural = 'Usuários-Tags'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.tag.nome}"


class UsuarioGrupo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usuario_id_usuario')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='grupo_id_grupo')
    
    class Meta:
        db_table = 'usuario_grupo'
        unique_together = ('usuario', 'grupo')
        verbose_name = 'Usuário-Grupo'
        verbose_name_plural = 'Usuários-Grupos'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.grupo.nome}"


class PerfilCliente(models.Model):
    id_perfil_cliente = models.AutoField(primary_key=True)
    CNH = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, db_column='usuario_id_usuario')
    
    class Meta:
        db_table = 'perfil_cliente'
        verbose_name = 'Perfil de Cliente'
        verbose_name_plural = 'Perfis de Clientes'
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"