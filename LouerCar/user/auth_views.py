# user/auth_views.py - SUBSTITUA O ARQUIVO COMPLETO

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, PerfilCliente
from .utils import atribuir_tags_automaticas, adicionar_usuario_em_grupo_automatico

def register(request):
    """Página de cadastro de novo usuário (Cliente)"""
    if request.method == 'POST':
        from .forms import UsuarioForm
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Criar usuário como cliente
            usuario = form.save(commit=False)
            usuario.is_staff = False
            usuario.is_superuser = False
            usuario.is_active = True
            usuario.save()
            
            # ⭐ ATRIBUIR TAGS AUTOMÁTICAS ⭐
            tags = atribuir_tags_automaticas(usuario)
            
            # ⭐ ADICIONAR EM GRUPOS AUTOMÁTICOS ⭐
            grupos = adicionar_usuario_em_grupo_automatico(usuario)
            
            messages.success(
                request, 
                f'✅ Cadastro realizado! Você recebeu {len(tags)} tag(s) e foi adicionado em {len(grupos)} grupo(s). Faça login para continuar.'
            )
            return redirect('login')
    else:
        from .forms import UsuarioForm
        form = UsuarioForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """Página de login"""
    # Se já está logado, redireciona direto
    if request.session.get('user_id'):
        if request.session.get('is_staff'):
            return redirect('dashboard_funcionario')
        else:
            return redirect('dashboard_cliente')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.get(username=username)
            if usuario.check_password(password):
                # Login manual
                request.session['user_id'] = usuario.id_usuario
                request.session['username'] = usuario.username
                request.session['is_staff'] = usuario.is_staff
                request.session['is_superuser'] = usuario.is_superuser
                
                messages.success(request, f'🎉 Bem-vindo, {usuario.username}!')
                
                # Redirecionar baseado no tipo
                if usuario.is_staff:
                    return redirect('dashboard_funcionario')
                else:
                    return redirect('dashboard_cliente')
            else:
                messages.error(request, '❌ Senha incorreta!')
        except Usuario.DoesNotExist:
            messages.error(request, '❌ Usuário não encontrado!')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Logout - LIMPA SESSÃO e redireciona para HOME"""
    username = request.session.get('username', 'Usuário')
    request.session.flush()
    messages.info(request, f'👋 Até logo, {username}! Você saiu do sistema.')
    return redirect('home')


def dashboard_cliente(request):
    """Dashboard do cliente - vê carros disponíveis e seus aluguéis"""
    if not request.session.get('user_id'):
        return redirect('login')
    
    if request.session.get('is_staff'):
        return redirect('dashboard_funcionario')
    
    from carro.models import Carro
    from aluguel.models import Aluguel
    
    user_id = request.session.get('user_id')
    
    try:
        usuario = Usuario.objects.get(id_usuario=user_id)
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, '❌ Sessão inválida. Faça login novamente.')
        return redirect('login')
    
    # Carros disponíveis
    carros_disponiveis = Carro.objects.filter(status='disponivel')
    
    # Aluguéis do cliente
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
        meus_alugueis = Aluguel.objects.filter(perfil_cliente=perfil).order_by('-criado_em')[:5]
    except PerfilCliente.DoesNotExist:
        perfil = None
        meus_alugueis = []
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
        'carros_disponiveis': carros_disponiveis,
        'meus_alugueis': meus_alugueis,
    }
    
    return render(request, 'auth/dashboard_cliente.html', context)


def dashboard_funcionario(request):
    """Dashboard do funcionário - acesso total"""
    if not request.session.get('user_id'):
        return redirect('login')
    
    if not request.session.get('is_staff'):
        messages.error(request, '❌ Acesso negado! Você não é funcionário.')
        return redirect('dashboard_cliente')
    
    from carro.models import Carro
    from aluguel.models import Aluguel
    
    user_id = request.session.get('user_id')
    
    try:
        usuario = Usuario.objects.get(id_usuario=user_id)
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, '❌ Sessão inválida. Faça login novamente.')
        return redirect('login')
    
    # Estatísticas
    total_carros = Carro.objects.count()
    carros_disponiveis = Carro.objects.filter(status='disponivel').count()
    carros_alugados = Carro.objects.filter(status='alugado').count()
    
    total_alugueis = Aluguel.objects.count()
    alugueis_ativos = Aluguel.objects.filter(status='ativo').count()
    
    total_clientes = Usuario.objects.filter(is_staff=False).count()
    
    context = {
        'usuario': usuario,
        'total_carros': total_carros,
        'carros_disponiveis': carros_disponiveis,
        'carros_alugados': carros_alugados,
        'total_alugueis': total_alugueis,
        'alugueis_ativos': alugueis_ativos,
        'total_clientes': total_clientes,
    }
    
    return render(request, 'auth/dashboard_funcionario.html', context)


def home(request):
    """Página inicial pública - Landing page"""
    from carro.models import Carro
    
    carros_destaque = Carro.objects.filter(status='disponivel')[:6]
    
    context = {
        'carros_destaque': carros_destaque,
    }
    
    return render(request, 'home.html', context)