# user/views.py - SUBSTITUA O ARQUIVO COMPLETO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario, PerfilCliente, Grupo, UsuarioGrupo, Tag, UsuarioTag
from .forms import (UsuarioForm, UsuarioUpdateForm, PerfilClienteForm, 
                    GrupoForm, UsuarioGrupoForm, TagForm, UsuarioTagForm)
from .decorators import admin_required, staff_required, cliente_required

# ========== VIEWS DE TAG (APENAS ADMIN) ==========

@admin_required
def tag_list(request):
    """Lista todas as tags - APENAS ADMIN"""
    tags = Tag.objects.all().order_by('nome')
    
    # Estatísticas
    for tag in tags:
        tag.total_usuarios = UsuarioTag.objects.filter(tag=tag).count()
        tag.total_grupos = Grupo.objects.filter(tag=tag).count()
    
    context = {
        'tags': tags,
    }
    
    return render(request, 'user/tag_list.html', context)


@admin_required
def tag_create(request):
    """Cria uma nova tag - APENAS ADMIN"""
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, f'✅ Tag "{tag.nome}" criada com sucesso!')
            return redirect('tag_list')
    else:
        form = TagForm()
    
    return render(request, 'user/tag_form.html', {
        'form': form,
        'title': 'Criar Nova Tag'
    })


@admin_required
def tag_update(request, pk):
    """Atualiza uma tag - APENAS ADMIN"""
    tag = get_object_or_404(Tag, pk=pk)
    
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save()
            messages.success(request, f'✅ Tag "{tag.nome}" atualizada com sucesso!')
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    
    return render(request, 'user/tag_form.html', {
        'form': form,
        'title': f'Editar Tag: {tag.nome}',
        'tag': tag
    })


@admin_required
def tag_delete(request, pk):
    """Deleta uma tag - APENAS ADMIN"""
    tag = get_object_or_404(Tag, pk=pk)
    
    if request.method == 'POST':
        nome = tag.nome
        tag.delete()
        messages.success(request, f'✅ Tag "{nome}" deletada com sucesso!')
        return redirect('tag_list')
    
    return render(request, 'user/tag_confirm_delete.html', {'tag': tag})


# ========== VIEWS DE USUÁRIO-TAG (APENAS ADMIN) ==========

@admin_required
def usuario_tag_create(request):
    """Atribui tag a um usuário - APENAS ADMIN"""
    if request.method == 'POST':
        form = UsuarioTagForm(request.POST)
        if form.is_valid():
            try:
                usuario_tag = form.save()
                messages.success(
                    request, 
                    f'✅ Tag "{usuario_tag.tag.nome}" atribuída a {usuario_tag.usuario.username}!'
                )
                return redirect('usuario_detail', pk=usuario_tag.usuario.id_usuario)
            except Exception as e:
                messages.error(request, f'❌ Erro: Este usuário já possui esta tag!')
    else:
        form = UsuarioTagForm()
    
    return render(request, 'user/usuario_tag_form.html', {
        'form': form,
        'title': 'Atribuir Tag ao Usuário'
    })


@admin_required
def usuario_tag_delete(request, pk):
    """Remove tag de um usuário - APENAS ADMIN"""
    usuario_tag = get_object_or_404(UsuarioTag, pk=pk)
    
    if request.method == 'POST':
        usuario = usuario_tag.usuario
        tag_nome = usuario_tag.tag.nome
        usuario_tag.delete()
        messages.success(request, f'✅ Tag "{tag_nome}" removida de {usuario.username}!')
        return redirect('usuario_detail', pk=usuario.id_usuario)
    
    return render(request, 'user/usuario_tag_confirm_delete.html', {
        'usuario_tag': usuario_tag
    })


# ========== VIEWS DE USUÁRIO (APENAS ADMIN) ==========

@admin_required
def usuario_list(request):
    """Lista todos os usuários - APENAS ADMIN"""
    usuarios = Usuario.objects.all().order_by('-data_cadastro')
    return render(request, 'user/usuario_list.html', {'usuarios': usuarios})


@admin_required
def usuario_create(request):
    """Cria um novo usuário - APENAS ADMIN"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            
            # ⭐ ATRIBUIR TAGS AUTOMÁTICAS ⭐
            from .utils import atribuir_tags_automaticas
            atribuir_tags_automaticas(usuario)
            
            messages.success(request, f'✅ Usuário "{usuario.username}" criado com tags automáticas!')
            return redirect('usuario_detail', pk=usuario.id_usuario)
    else:
        form = UsuarioForm()
    return render(request, 'user/usuario_form.html', {'form': form, 'title': 'Criar Usuário'})


@admin_required
def usuario_update(request, pk):
    """Atualiza um usuário existente - APENAS ADMIN"""
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_atualizado = form.save()
            
            # ⭐ ATUALIZAR TAGS SE MUDOU FUNÇÃO ⭐
            from .utils import atualizar_tags_por_funcao
            atualizar_tags_por_funcao(usuario_atualizado)
            
            messages.success(request, f'✅ Usuário "{usuario.username}" atualizado!')
            return redirect('usuario_detail', pk=usuario.id_usuario)
    else:
        form = UsuarioUpdateForm(instance=usuario)
    return render(request, 'user/usuario_form.html', {'form': form, 'title': 'Editar Usuário'})


@admin_required
def usuario_delete(request, pk):
    """Deleta um usuário - APENAS ADMIN"""
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'✅ Usuário "{username}" deletado!')
        return redirect('usuario_list')
    return render(request, 'user/usuario_confirm_delete.html', {'usuario': usuario})


@admin_required
def usuario_detail(request, pk):
    """Exibe detalhes de um usuário - APENAS ADMIN"""
    usuario = get_object_or_404(Usuario, pk=pk)
    
    # Buscar tags
    tags = UsuarioTag.objects.filter(usuario=usuario).select_related('tag')
    
    # Buscar grupos
    grupos = UsuarioGrupo.objects.filter(usuario=usuario).select_related('grupo')
    
    # Buscar perfil
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
    except PerfilCliente.DoesNotExist:
        perfil = None
    
    return render(request, 'user/usuario_detail.html', {
        'usuario': usuario,
        'tags': tags,
        'grupos': grupos,
        'perfil': perfil
    })


# ========== VIEWS DE PERFIL CLIENTE (APENAS ADMIN) ==========

@admin_required
def perfil_list(request):
    """Lista todos os perfis de clientes - APENAS ADMIN"""
    perfis = PerfilCliente.objects.all().order_by('-criado_em')
    return render(request, 'user/perfil_list.html', {'perfis': perfis})


@cliente_required
def perfil_create(request):
    """Cria um novo perfil de cliente - QUALQUER USUÁRIO"""
    if request.method == 'POST':
        form = PerfilClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Perfil criado com sucesso!')
            return redirect('dashboard_cliente')
    else:
        form = PerfilClienteForm()
    return render(request, 'user/perfil_form.html', {'form': form, 'title': 'Criar Perfil de Cliente'})


@admin_required
def perfil_update(request, pk):
    """Atualiza um perfil de cliente - APENAS ADMIN"""
    perfil = get_object_or_404(PerfilCliente, pk=pk)
    if request.method == 'POST':
        form = PerfilClienteForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Perfil atualizado!')
            return redirect('perfil_list')
    else:
        form = PerfilClienteForm(instance=perfil)
    return render(request, 'user/perfil_form.html', {'form': form, 'title': 'Editar Perfil'})


@admin_required
def perfil_delete(request, pk):
    """Deleta um perfil de cliente - APENAS ADMIN"""
    perfil = get_object_or_404(PerfilCliente, pk=pk)
    if request.method == 'POST':
        perfil.delete()
        messages.success(request, '✅ Perfil deletado!')
        return redirect('perfil_list')
    return render(request, 'user/perfil_confirm_delete.html', {'perfil': perfil})


@admin_required
def perfil_detail(request, pk):
    """Exibe detalhes de um perfil - APENAS ADMIN"""
    perfil = get_object_or_404(PerfilCliente, pk=pk)
    return render(request, 'user/perfil_detail.html', {'perfil': perfil})


# ========== VIEWS DE GRUPO (APENAS ADMIN) ==========

@admin_required
def grupo_list(request):
    """Lista todos os grupos - APENAS ADMIN"""
    grupos = Grupo.objects.all().select_related('tag').order_by('nome')
    return render(request, 'user/grupo_list.html', {'grupos': grupos})


@admin_required
def grupo_create(request):
    """Cria um novo grupo - APENAS ADMIN"""
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save()
            messages.success(request, f'✅ Grupo "{grupo.nome}" criado!')
            return redirect('grupo_list')
    else:
        form = GrupoForm()
    return render(request, 'user/grupo_form.html', {'form': form, 'title': 'Criar Grupo'})


@admin_required
def grupo_update(request, pk):
    """Atualiza um grupo - APENAS ADMIN"""
    grupo = get_object_or_404(Grupo, pk=pk)
    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            grupo = form.save()
            messages.success(request, f'✅ Grupo "{grupo.nome}" atualizado!')
            return redirect('grupo_list')
    else:
        form = GrupoForm(instance=grupo)
    return render(request, 'user/grupo_form.html', {'form': form, 'title': 'Editar Grupo'})


@admin_required
def grupo_delete(request, pk):
    """Deleta um grupo - APENAS ADMIN"""
    grupo = get_object_or_404(Grupo, pk=pk)
    if request.method == 'POST':
        nome = grupo.nome
        grupo.delete()
        messages.success(request, f'✅ Grupo "{nome}" deletado!')
        return redirect('grupo_list')
    return render(request, 'user/grupo_confirm_delete.html', {'grupo': grupo})


# ========== VIEWS DE USUÁRIO-GRUPO (APENAS ADMIN) ==========

@admin_required
def usuario_grupo_create(request):
    """Adiciona um usuário a um grupo - APENAS ADMIN"""
    if request.method == 'POST':
        form = UsuarioGrupoForm(request.POST)
        if form.is_valid():
            ug = form.save()
            messages.success(request, f'✅ {ug.usuario.username} adicionado ao grupo {ug.grupo.nome}!')
            return redirect('usuario_detail', pk=ug.usuario.id_usuario)
    else:
        form = UsuarioGrupoForm()
    return render(request, 'user/usuario_grupo_form.html', {'form': form, 'title': 'Adicionar ao Grupo'})


@admin_required
def usuario_grupo_delete(request, pk):
    """Remove um usuário de um grupo - APENAS ADMIN"""
    usuario_grupo = get_object_or_404(UsuarioGrupo, pk=pk)
    if request.method == 'POST':
        usuario = usuario_grupo.usuario
        usuario_grupo.delete()
        messages.success(request, '✅ Usuário removido do grupo!')
        return redirect('usuario_detail', pk=usuario.id_usuario)
    return render(request, 'user/usuario_grupo_confirm_delete.html', {'usuario_grupo': usuario_grupo})


# ========== MEU PERFIL ==========

@cliente_required
def meu_perfil(request):
    """Exibe o perfil completo do usuário logado"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    # Buscar perfil
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
    except PerfilCliente.DoesNotExist:
        perfil = None
    
    # Buscar tags
    tags = UsuarioTag.objects.filter(usuario=usuario).select_related('tag')
    
    # Buscar grupos
    grupos = UsuarioGrupo.objects.filter(usuario=usuario).select_related('grupo')
    
    # Buscar aluguéis
    from aluguel.models import Aluguel
    if perfil:
        alugueis = Aluguel.objects.filter(perfil_cliente=perfil).order_by('-criado_em')[:5]
    else:
        alugueis = []
    
    # Aluguéis gerenciados (funcionário)
    if usuario.is_staff:
        alugueis_gerenciados = Aluguel.objects.filter(funcionario=usuario).order_by('-criado_em')[:5]
    else:
        alugueis_gerenciados = []
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
        'tags': tags,
        'grupos': grupos,
        'alugueis': alugueis,
        'alugueis_gerenciados': alugueis_gerenciados,
    }
    
    return render(request, 'user/meu_perfil.html', context)


@cliente_required
def editar_meu_perfil(request):
    """Permite que qualquer usuário edite seu próprio perfil"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
    except PerfilCliente.DoesNotExist:
        perfil = None
    
    if request.method == 'POST':
        usuario.email = request.POST.get('email', usuario.email)
        usuario.foto_perfil = request.POST.get('foto_perfil', usuario.foto_perfil)
        
        nova_senha = request.POST.get('password')
        if nova_senha:
            usuario.set_password(nova_senha)
        
        usuario.save()
        
        if not usuario.is_staff:
            cnh = request.POST.get('CNH')
            telefone = request.POST.get('telefone')
            endereco = request.POST.get('endereco')
            
            if cnh and telefone and endereco:
                if perfil:
                    perfil.CNH = cnh
                    perfil.telefone = telefone
                    perfil.endereco = endereco
                    perfil.save()
                else:
                    perfil = PerfilCliente.objects.create(
                        usuario=usuario,
                        CNH=cnh,
                        telefone=telefone,
                        endereco=endereco
                    )
        
        messages.success(request, '✅ Perfil atualizado com sucesso!')
        return redirect('meu_perfil')
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
    }
    
    return render(request, 'user/editar_meu_perfil.html', context)


# ========== MEUS GRUPOS ==========

# user/views.py - SUBSTITUA APENAS A FUNÇÃO meus_grupos

@cliente_required
def meus_grupos(request):
    """Exibe grupos visíveis baseado nas tags do usuário"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    # Tags do usuário
    tags_usuario = usuario.tags.all()
    
    # DEBUG: Verificar se tem tags
    print(f"🔍 DEBUG - Usuário: {usuario.username}")
    print(f"🔍 DEBUG - Total de tags: {tags_usuario.count()}")
    for tag in tags_usuario:
        print(f"   - Tag: {tag.nome}")
    
    # Grupos visíveis baseado nas tags
    if tags_usuario.exists():
        grupos_visiveis = Grupo.objects.filter(tag__in=tags_usuario).distinct()
    else:
        # Se não tem tags, não vê nenhum grupo
        grupos_visiveis = Grupo.objects.none()
    
    # DEBUG: Verificar grupos
    print(f"🔍 DEBUG - Total de grupos visíveis: {grupos_visiveis.count()}")
    for grupo in grupos_visiveis:
        print(f"   - Grupo: {grupo.nome} (Tag: {grupo.tag.nome if grupo.tag else 'Sem tag'})")
    
    # Grupos que já participa
    grupos_participando = UsuarioGrupo.objects.filter(
        usuario=usuario
    ).values_list('grupo_id', flat=True)
    
    context = {
        'tags': tags_usuario,
        'grupos': grupos_visiveis,
        'grupos_participando': list(grupos_participando),
    }
    
    return render(request, 'user/meus_grupos.html', context)

@cliente_required
def entrar_grupo(request, grupo_id):
    """Adiciona usuário ao grupo"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    
    # Verificar tag
    if grupo.tag and grupo.tag not in usuario.get_tags():
        messages.error(request, '❌ Você não tem permissão para entrar neste grupo!')
        return redirect('meus_grupos')
    
    # Verificar se já está
    if UsuarioGrupo.objects.filter(usuario=usuario, grupo=grupo).exists():
        messages.warning(request, '⚠️ Você já está neste grupo!')
        return redirect('meus_grupos')
    
    # Adicionar
    UsuarioGrupo.objects.create(usuario=usuario, grupo=grupo)
    messages.success(request, f'✅ Você entrou no grupo "{grupo.nome}"!')
    
    # Redirecionar para WhatsApp se disponível
    if grupo.link_whatsapp:
        return redirect(grupo.link_whatsapp)
    
    return redirect('meus_grupos')