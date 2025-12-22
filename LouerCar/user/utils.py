# user/utils.py - CRIAR ESTE ARQUIVO NOVO

from .models import Tag, UsuarioTag, Grupo, UsuarioGrupo

def criar_tags_padrao():
    """
    Cria tags padrão do sistema se não existirem
    """
    tags_padrao = [
        {
            'nome': 'Cliente Novo',
            'cor': 'success',
            'icone': 'bi-star-fill',
            'descricao': 'Clientes que acabaram de se cadastrar'
        },
        {
            'nome': 'Cliente VIP',
            'cor': 'warning',
            'icone': 'bi-award-fill',
            'descricao': 'Clientes premium com benefícios exclusivos'
        },
        {
            'nome': 'Funcionário',
            'cor': 'info',
            'icone': 'bi-person-badge-fill',
            'descricao': 'Funcionários da empresa'
        },
        {
            'nome': 'Administrador',
            'cor': 'danger',
            'icone': 'bi-shield-fill-check',
            'descricao': 'Administradores do sistema'
        },
    ]
    
    tags_criadas = []
    for tag_data in tags_padrao:
        tag, created = Tag.objects.get_or_create(
            nome=tag_data['nome'],
            defaults={
                'cor': tag_data['cor'],
                'icone': tag_data['icone'],
                'descricao': tag_data['descricao']
            }
        )
        if created:
            tags_criadas.append(tag.nome)
    
    return tags_criadas


def criar_grupos_padrao():
    """
    Cria grupos padrão do sistema
    """
    # Garantir que as tags existem
    criar_tags_padrao()
    
    grupos_padrao = [
        {
            'nome': 'Grupo de Boas-Vindas - Clientes Novos',
            'descricao': 'Bem-vindo à LouerCar! Aqui você receberá dicas e suporte inicial.',
            'tag_nome': 'Cliente Novo',
            'link_whatsapp': 'https://chat.whatsapp.com/exemplo-clientes-novos'
        },
        {
            'nome': 'Grupo VIP - Benefícios Exclusivos',
            'descricao': 'Grupo exclusivo para clientes VIP com promoções especiais.',
            'tag_nome': 'Cliente VIP',
            'link_whatsapp': 'https://chat.whatsapp.com/exemplo-vip'
        },
        {
            'nome': 'Equipe LouerCar - Funcionários',
            'descricao': 'Comunicação interna da equipe de funcionários.',
            'tag_nome': 'Funcionário',
            'link_whatsapp': 'https://chat.whatsapp.com/exemplo-funcionarios'
        },
    ]
    
    grupos_criados = []
    for grupo_data in grupos_padrao:
        try:
            tag = Tag.objects.get(nome=grupo_data['tag_nome'])
            grupo, created = Grupo.objects.get_or_create(
                nome=grupo_data['nome'],
                defaults={
                    'descricao': grupo_data['descricao'],
                    'tag': tag,
                    'link_whatsapp': grupo_data['link_whatsapp']
                }
            )
            if created:
                grupos_criados.append(grupo.nome)
        except Tag.DoesNotExist:
            pass
    
    return grupos_criados


def atribuir_tags_automaticas(usuario):
    """
    Atribui tags automaticamente ao usuário baseado em sua função
    """
    tags_atribuidas = []
    
    # ADMINISTRADOR
    if usuario.is_superuser:
        try:
            tag_admin = Tag.objects.get(nome='Administrador')
            UsuarioTag.objects.get_or_create(usuario=usuario, tag=tag_admin)
            tags_atribuidas.append('Administrador')
        except Tag.DoesNotExist:
            pass
    
    # FUNCIONÁRIO
    if usuario.is_staff:
        try:
            tag_func = Tag.objects.get(nome='Funcionário')
            UsuarioTag.objects.get_or_create(usuario=usuario, tag=tag_func)
            tags_atribuidas.append('Funcionário')
        except Tag.DoesNotExist:
            pass
    
    # CLIENTE NOVO
    if not usuario.is_staff and not usuario.is_superuser:
        try:
            tag_cliente = Tag.objects.get(nome='Cliente Novo')
            UsuarioTag.objects.get_or_create(usuario=usuario, tag=tag_cliente)
            tags_atribuidas.append('Cliente Novo')
        except Tag.DoesNotExist:
            pass
    
    return tags_atribuidas


def atualizar_tags_por_funcao(usuario):
    """
    Atualiza tags quando a função do usuário muda
    """
    # Remover todas as tags de função antiga
    tags_funcao = ['Cliente Novo', 'Cliente VIP', 'Funcionário', 'Administrador']
    UsuarioTag.objects.filter(
        usuario=usuario,
        tag__nome__in=tags_funcao
    ).delete()
    
    # Atribuir novas tags
    return atribuir_tags_automaticas(usuario)


def adicionar_usuario_em_grupo_automatico(usuario):
    """
    Adiciona usuário automaticamente nos grupos de sua tag
    """
    grupos_adicionados = []
    tags_usuario = usuario.get_tags()
    
    for tag in tags_usuario:
        # Buscar grupos desta tag
        grupos = Grupo.objects.filter(tag=tag)
        
        for grupo in grupos:
            # Verificar se já não está no grupo
            ug, created = UsuarioGrupo.objects.get_or_create(
                usuario=usuario,
                grupo=grupo
            )
            if created:
                grupos_adicionados.append(grupo.nome)
    
    return grupos_adicionados