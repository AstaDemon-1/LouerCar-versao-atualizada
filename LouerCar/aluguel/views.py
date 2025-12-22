from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum, Count
from .models import Aluguel, SolicitacaoAluguel
from .forms import AluguelForm, SolicitacaoAluguelForm
from carro.models import Carro
from user.models import PerfilCliente, Usuario
from user.decorators import staff_required, cliente_required

# ============================================
# VIEWS PARA CLIENTES (Solicitações)
# ============================================

@cliente_required
def solicitar_aluguel(request, carro_id=None):
    """Cliente solicita aluguel - PRECISA TER PERFIL COMPLETO"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    # Verificar se tem perfil completo
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
    except PerfilCliente.DoesNotExist:
        messages.warning(
            request, 
            'Você precisa completar seu perfil antes de solicitar um aluguel!'
        )
        return redirect('perfil_create')
    
    # Pegar o carro se foi especificado
    carro = None
    if carro_id:
        carro = get_object_or_404(Carro, id_carro=carro_id)
        if carro.status != 'disponivel':
            messages.error(request, f'O carro {carro.modelo} não está disponível!')
            return redirect('carro_list')
    
    if request.method == 'POST':
        form = SolicitacaoAluguelForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.perfil_cliente = perfil
            
            # Calcular valor estimado
            dias = solicitacao.calcular_dias()
            solicitacao.valor_estimado = solicitacao.carro.preco_diaria * dias
            
            solicitacao.save()
            
            messages.success(
                request, 
                f'Solicitação enviada com sucesso! Aguarde a aprovação do funcionário.'
            )
            return redirect('minhas_solicitacoes')
    else:
        initial_data = {}
        if carro:
            initial_data['carro'] = carro
        form = SolicitacaoAluguelForm(initial=initial_data)
    
    return render(request, 'aluguel/solicitar_aluguel.html', {
        'form': form,
        'carro': carro,
        'perfil': perfil,
    })


@cliente_required
def minhas_solicitacoes(request):
    """Cliente vê suas solicitações"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
        solicitacoes = SolicitacaoAluguel.objects.filter(
            perfil_cliente=perfil
        ).select_related('carro').order_by('-criado_em')
    except PerfilCliente.DoesNotExist:
        solicitacoes = []
    
    context = {
        'solicitacoes': solicitacoes,
    }
    
    return render(request, 'aluguel/minhas_solicitacoes.html', context)


@cliente_required
def cancelar_solicitacao(request, pk):
    """Cliente cancela sua solicitação"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
        solicitacao = get_object_or_404(
            SolicitacaoAluguel, 
            pk=pk, 
            perfil_cliente=perfil
        )
        
        if solicitacao.status == 'pendente':
            if request.method == 'POST':
                solicitacao.status = 'cancelado'
                solicitacao.save()
                messages.info(request, 'Solicitação cancelada com sucesso!')
                return redirect('minhas_solicitacoes')
            
            return render(request, 'aluguel/cancelar_solicitacao.html', {
                'solicitacao': solicitacao
            })
        else:
            messages.error(request, 'Não é possível cancelar esta solicitação!')
            return redirect('minhas_solicitacoes')
            
    except PerfilCliente.DoesNotExist:
        messages.error(request, 'Perfil não encontrado!')
        return redirect('dashboard_cliente')


# ============================================
# VIEWS PARA FUNCIONÁRIOS (Aprovar/Rejeitar)
# ============================================

@staff_required
def solicitacoes_pendentes(request):
    """Funcionário vê solicitações pendentes"""
    solicitacoes = SolicitacaoAluguel.objects.filter(
        status='pendente'
    ).select_related('perfil_cliente', 'carro', 'perfil_cliente__usuario').order_by('-criado_em')
    
    # Estatísticas
    total_pendentes = solicitacoes.count()
    total_aprovadas = SolicitacaoAluguel.objects.filter(status='aprovado').count()
    total_rejeitadas = SolicitacaoAluguel.objects.filter(status='rejeitado').count()
    
    context = {
        'solicitacoes': solicitacoes,
        'total_pendentes': total_pendentes,
        'total_aprovadas': total_aprovadas,
        'total_rejeitadas': total_rejeitadas,
    }
    
    return render(request, 'aluguel/solicitacoes_pendentes.html', context)


@staff_required
def aprovar_solicitacao(request, pk):
    """Funcionário aprova solicitação e cria aluguel"""
    solicitacao = get_object_or_404(SolicitacaoAluguel, pk=pk)
    
    if solicitacao.status != 'pendente':
        messages.error(request, 'Esta solicitação não está pendente!')
        return redirect('solicitacoes_pendentes')
    
    if request.method == 'POST':
        # Criar o aluguel oficial
        user_id = request.session.get('user_id')
        funcionario = get_object_or_404(Usuario, id_usuario=user_id)
        
        aluguel = Aluguel.objects.create(
            perfil_cliente=solicitacao.perfil_cliente,
            carro=solicitacao.carro,
            funcionario=funcionario,
            data_inicio=solicitacao.data_inicio,
            data_fim=solicitacao.data_fim,
            valor=solicitacao.valor_estimado,
            status='ativo'
        )
        
        # Atualizar solicitação
        solicitacao.status = 'aprovado'
        solicitacao.aluguel_criado = aluguel
        solicitacao.save()
        
        messages.success(
            request, 
            f'Solicitação aprovada! Aluguel #{aluguel.id_aluguel} criado com sucesso.'
        )
        return redirect('aluguel_detail', pk=aluguel.id_aluguel)
    
    return render(request, 'aluguel/aprovar_solicitacao.html', {
        'solicitacao': solicitacao
    })


@staff_required
def rejeitar_solicitacao(request, pk):
    """Funcionário rejeita solicitação"""
    solicitacao = get_object_or_404(SolicitacaoAluguel, pk=pk)
    
    if solicitacao.status != 'pendente':
        messages.error(request, 'Esta solicitação não está pendente!')
        return redirect('solicitacoes_pendentes')
    
    if request.method == 'POST':
        solicitacao.status = 'rejeitado'
        solicitacao.save()
        
        messages.warning(request, 'Solicitação rejeitada!')
        return redirect('solicitacoes_pendentes')
    
    return render(request, 'aluguel/rejeitar_solicitacao.html', {
        'solicitacao': solicitacao
    })


# ============================================
# VIEWS ORIGINAIS DE ALUGUEL (Funcionários)
# ============================================

@staff_required
def aluguel_list(request):
    """Lista todos os aluguéis com filtros"""
    alugueis = Aluguel.objects.all().select_related('carro', 'perfil_cliente', 'funcionario')
    
    # Filtro de busca
    query = request.GET.get('q')
    if query:
        alugueis = alugueis.filter(
            Q(carro__modelo__icontains=query) |
            Q(carro__placa__icontains=query) |
            Q(perfil_cliente__usuario__username__icontains=query) |
            Q(perfil_cliente__CNH__icontains=query)
        )
    
    # Filtro por status
    status_filter = request.GET.get('status')
    if status_filter:
        alugueis = alugueis.filter(status=status_filter)
    
    # Estatísticas
    total_alugueis = Aluguel.objects.count()
    ativos = Aluguel.objects.filter(status='ativo').count()
    finalizados = Aluguel.objects.filter(status='finalizado').count()
    cancelados = Aluguel.objects.filter(status='cancelado').count()
    
    # Valor total em aluguéis ativos
    valor_total_ativos = Aluguel.objects.filter(status='ativo').aggregate(
        total=Sum('valor')
    )['total'] or 0
    
    context = {
        'alugueis': alugueis,
        'total_alugueis': total_alugueis,
        'ativos': ativos,
        'finalizados': finalizados,
        'cancelados': cancelados,
        'valor_total_ativos': valor_total_ativos,
        'query': query,
        'status_filter': status_filter,
    }
    
    return render(request, 'aluguel/aluguel_list.html', context)


@staff_required
def aluguel_create(request):
    """Cria um novo aluguel (FUNCIONÁRIO CRIA MANUALMENTE)"""
    if request.method == 'POST':
        form = AluguelForm(request.POST)
        if form.is_valid():
            aluguel = form.save()
            messages.success(
                request, 
                f'Aluguel #{aluguel.id_aluguel} registrado com sucesso!'
            )
            return redirect('aluguel_list')
    else:
        form = AluguelForm()
    
    return render(request, 'aluguel/aluguel_form.html', {
        'form': form,
        'title': 'Registrar Novo Aluguel'
    })


@staff_required
def aluguel_update(request, pk):
    """Atualiza um aluguel existente"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        form = AluguelForm(request.POST, instance=aluguel)
        if form.is_valid():
            aluguel = form.save()
            messages.success(
                request, 
                f'Aluguel #{aluguel.id_aluguel} atualizado com sucesso!'
            )
            return redirect('aluguel_detail', pk=aluguel.pk)
    else:
        form = AluguelForm(instance=aluguel)
    
    return render(request, 'aluguel/aluguel_form.html', {
        'form': form,
        'title': f'Editar Aluguel #{aluguel.id_aluguel}',
        'aluguel': aluguel
    })


@staff_required
def aluguel_delete(request, pk):
    """Deleta um aluguel"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        id_aluguel = aluguel.id_aluguel
        carro = aluguel.carro
        
        # Se era um aluguel ativo, liberar o carro
        if aluguel.status == 'ativo':
            carro.status = 'disponivel'
            carro.save()
        
        aluguel.delete()
        messages.success(request, f'Aluguel #{id_aluguel} deletado com sucesso!')
        return redirect('aluguel_list')
    
    return render(request, 'aluguel/aluguel_confirm_delete.html', {'aluguel': aluguel})


@cliente_required
def aluguel_detail(request, pk):
    """Exibe detalhes de um aluguel (CLIENTE e FUNCIONÁRIO)"""
    aluguel = get_object_or_404(
        Aluguel.objects.select_related('carro', 'perfil_cliente', 'funcionario'),
        pk=pk
    )
    
    # Verificar se é o cliente dono do aluguel ou funcionário
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    # Cliente só vê seus próprios aluguéis
    if not usuario.is_staff:
        try:
            perfil = PerfilCliente.objects.get(usuario=usuario)
            if aluguel.perfil_cliente != perfil:
                messages.error(request, 'Você não tem permissão para ver este aluguel!')
                return redirect('dashboard_cliente')
        except PerfilCliente.DoesNotExist:
            messages.error(request, 'Perfil não encontrado!')
            return redirect('dashboard_cliente')
    
    context = {
        'aluguel': aluguel,
    }
    
    return render(request, 'aluguel/aluguel_detail.html', context)


@staff_required
def aluguel_change_status(request, pk):
    """Altera o status do aluguel"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        
        if novo_status in ['ativo', 'finalizado', 'cancelado']:
            aluguel.status = novo_status
            aluguel.save()
            
            status_messages = {
                'ativo': ('info', 'ATIVO'),
                'finalizado': ('success', 'FINALIZADO'),
                'cancelado': ('warning', 'CANCELADO'),
            }
            
            msg_type, msg_status = status_messages.get(novo_status, ('info', 'ATUALIZADO'))
            
            if msg_type == 'success':
                messages.success(request, f'Aluguel #{aluguel.id_aluguel} marcado como {msg_status}')
            elif msg_type == 'warning':
                messages.warning(request, f'Aluguel #{aluguel.id_aluguel} marcado como {msg_status}')
            else:
                messages.info(request, f'Aluguel #{aluguel.id_aluguel} marcado como {msg_status}')
        
        return redirect('aluguel_detail', pk=aluguel.pk)
    
    return redirect('aluguel_list')


@staff_required
def aluguel_finalizar(request, pk):
    """Finaliza um aluguel ativo"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        if aluguel.status == 'ativo':
            aluguel.status = 'finalizado'
            aluguel.save()
            messages.success(request, f'Aluguel #{aluguel.id_aluguel} finalizado com sucesso!')
        else:
            messages.warning(request, 'Este aluguel não está ativo!')
        
        return redirect('aluguel_detail', pk=aluguel.pk)
    
    return render(request, 'aluguel/aluguel_finalizar.html', {'aluguel': aluguel})


@staff_required
def aluguel_cancelar(request, pk):
    """Cancela um aluguel"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum, Count
from .models import Aluguel, SolicitacaoAluguel
from .forms import AluguelForm, SolicitacaoAluguelForm
from carro.models import Carro
from user.models import PerfilCliente, Usuario
from user.decorators import staff_required, cliente_required

# ============================================
# VIEWS PARA CLIENTES (Solicitações)
# ============================================

@cliente_required
def solicitar_aluguel(request, carro_id=None):
    """Cliente solicita aluguel - PRECISA TER PERFIL COMPLETO"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    # Verificar se tem perfil completo
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
    except PerfilCliente.DoesNotExist:
        messages.warning(
            request, 
            'Você precisa completar seu perfil antes de solicitar um aluguel!'
        )
        return redirect('perfil_create')
    
    # Pegar o carro se foi especificado
    carro = None
    if carro_id:
        carro = get_object_or_404(Carro, id_carro=carro_id)
        if carro.status != 'disponivel':
            messages.error(request, f'O carro {carro.modelo} não está disponível!')
            return redirect('carro_list')
    
    if request.method == 'POST':
        form = SolicitacaoAluguelForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.perfil_cliente = perfil
            
            # Calcular valor estimado
            dias = solicitacao.calcular_dias()
            solicitacao.valor_estimado = solicitacao.carro.preco_diaria * dias
            
            solicitacao.save()
            
            messages.success(
                request, 
                f'Solicitação enviada com sucesso! Aguarde a aprovação do funcionário.'
            )
            return redirect('minhas_solicitacoes')
    else:
        initial_data = {}
        if carro:
            initial_data['carro'] = carro
        form = SolicitacaoAluguelForm(initial=initial_data)
    
    return render(request, 'aluguel/solicitar_aluguel.html', {
        'form': form,
        'carro': carro,
        'perfil': perfil,
    })


@cliente_required
def minhas_solicitacoes(request):
    """Cliente vê suas solicitações"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
        solicitacoes = SolicitacaoAluguel.objects.filter(
            perfil_cliente=perfil
        ).select_related('carro').order_by('-criado_em')
    except PerfilCliente.DoesNotExist:
        solicitacoes = []
    
    context = {
        'solicitacoes': solicitacoes,
    }
    
    return render(request, 'aluguel/minhas_solicitacoes.html', context)


@cliente_required
def cancelar_solicitacao(request, pk):
    """Cliente cancela sua solicitação"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
        solicitacao = get_object_or_404(
            SolicitacaoAluguel, 
            pk=pk, 
            perfil_cliente=perfil
        )
        
        if solicitacao.status == 'pendente':
            if request.method == 'POST':
                solicitacao.status = 'cancelado'
                solicitacao.save()
                messages.info(request, 'Solicitação cancelada com sucesso!')
                return redirect('minhas_solicitacoes')
            
            return render(request, 'aluguel/cancelar_solicitacao.html', {
                'solicitacao': solicitacao
            })
        else:
            messages.error(request, 'Não é possível cancelar esta solicitação!')
            return redirect('minhas_solicitacoes')
            
    except PerfilCliente.DoesNotExist:
        messages.error(request, 'Perfil não encontrado!')
        return redirect('dashboard_cliente')


# ============================================
# VIEWS PARA FUNCIONÁRIOS (Aprovar/Rejeitar)
# ============================================

@staff_required
def solicitacoes_pendentes(request):
    """Funcionário vê solicitações pendentes"""
    solicitacoes = SolicitacaoAluguel.objects.filter(
        status='pendente'
    ).select_related('perfil_cliente', 'carro', 'perfil_cliente__usuario').order_by('-criado_em')
    
    # Estatísticas
    total_pendentes = solicitacoes.count()
    total_aprovadas = SolicitacaoAluguel.objects.filter(status='aprovado').count()
    total_rejeitadas = SolicitacaoAluguel.objects.filter(status='rejeitado').count()
    
    context = {
        'solicitacoes': solicitacoes,
        'total_pendentes': total_pendentes,
        'total_aprovadas': total_aprovadas,
        'total_rejeitadas': total_rejeitadas,
    }
    
    return render(request, 'aluguel/solicitacoes_pendentes.html', context)


@staff_required
def aprovar_solicitacao(request, pk):
    """Funcionário aprova solicitação e cria aluguel"""
    solicitacao = get_object_or_404(SolicitacaoAluguel, pk=pk)
    
    if solicitacao.status != 'pendente':
        messages.error(request, 'Esta solicitação não está mais pendente!')
        return redirect('solicitacoes_pendentes')
    
    if request.method == 'POST':
        # Criar o aluguel oficial
        user_id = request.session.get('user_id')
        funcionario = get_object_or_404(Usuario, id_usuario=user_id)
        
        aluguel = Aluguel.objects.create(
            perfil_cliente=solicitacao.perfil_cliente,
            carro=solicitacao.carro,
            funcionario=funcionario,
            data_inicio=solicitacao.data_inicio,
            data_fim=solicitacao.data_fim,
            valor=solicitacao.valor_estimado,
            status='ativo'
        )
        
        # Atualizar solicitação
        solicitacao.status = 'aprovado'
        solicitacao.aluguel_criado = aluguel
        solicitacao.save()
        
        messages.success(
            request, 
            f'✅ Solicitação aprovada! Aluguel #{aluguel.id_aluguel} criado com sucesso.'
        )
        return redirect('solicitacoes_pendentes')
    
    return render(request, 'aluguel/aprovar_solicitacao.html', {
        'solicitacao': solicitacao
    })


@staff_required
def rejeitar_solicitacao(request, pk):
    """Funcionário rejeita solicitação - ÚNICA FORMA"""
    solicitacao = get_object_or_404(SolicitacaoAluguel, pk=pk)
    
    if solicitacao.status != 'pendente':
        messages.error(request, 'Esta solicitação não está mais pendente!')
        return redirect('solicitacoes_pendentes')
    
    if request.method == 'POST':
        solicitacao.status = 'rejeitado'
        solicitacao.save()
        
        messages.warning(
            request, 
            f'❌ Solicitação #{solicitacao.id_solicitacao} rejeitada!'
        )
        return redirect('solicitacoes_pendentes')
    
    return render(request, 'aluguel/rejeitar_solicitacao.html', {
        'solicitacao': solicitacao
    })


# ============================================
# VIEWS ORIGINAIS DE ALUGUEL (Funcionários)
# ============================================

@staff_required
def aluguel_list(request):
    """Lista todos os aluguéis com filtros"""
    alugueis = Aluguel.objects.all().select_related('carro', 'perfil_cliente', 'funcionario')
    
    # Filtro de busca
    query = request.GET.get('q')
    if query:
        alugueis = alugueis.filter(
            Q(carro__modelo__icontains=query) |
            Q(carro__placa__icontains=query) |
            Q(perfil_cliente__usuario__username__icontains=query) |
            Q(perfil_cliente__CNH__icontains=query)
        )
    
    # Filtro por status
    status_filter = request.GET.get('status')
    if status_filter:
        alugueis = alugueis.filter(status=status_filter)
    
    # Estatísticas
    total_alugueis = Aluguel.objects.count()
    ativos = Aluguel.objects.filter(status='ativo').count()
    finalizados = Aluguel.objects.filter(status='finalizado').count()
    cancelados = Aluguel.objects.filter(status='cancelado').count()
    
    # Valor total em aluguéis ativos
    valor_total_ativos = Aluguel.objects.filter(status='ativo').aggregate(
        total=Sum('valor')
    )['total'] or 0
    
    context = {
        'alugueis': alugueis,
        'total_alugueis': total_alugueis,
        'ativos': ativos,
        'finalizados': finalizados,
        'cancelados': cancelados,
        'valor_total_ativos': valor_total_ativos,
        'query': query,
        'status_filter': status_filter,
    }
    
    return render(request, 'aluguel/aluguel_list.html', context)


@staff_required
def aluguel_create(request):
    """Cria um novo aluguel (FUNCIONÁRIO CRIA MANUALMENTE)"""
    if request.method == 'POST':
        form = AluguelForm(request.POST)
        if form.is_valid():
            aluguel = form.save()
            messages.success(
                request, 
                f'Aluguel #{aluguel.id_aluguel} registrado com sucesso!'
            )
            return redirect('aluguel_list')
    else:
        form = AluguelForm()
    
    return render(request, 'aluguel/aluguel_form.html', {
        'form': form,
        'title': 'Registrar Novo Aluguel'
    })


@staff_required
def aluguel_update(request, pk):
    """Atualiza um aluguel existente"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        form = AluguelForm(request.POST, instance=aluguel)
        if form.is_valid():
            aluguel = form.save()
            messages.success(
                request, 
                f'Aluguel #{aluguel.id_aluguel} atualizado com sucesso!'
            )
            return redirect('aluguel_detail', pk=aluguel.pk)
    else:
        form = AluguelForm(instance=aluguel)
    
    return render(request, 'aluguel/aluguel_form.html', {
        'form': form,
        'title': f'Editar Aluguel #{aluguel.id_aluguel}',
        'aluguel': aluguel
    })


@staff_required
def aluguel_delete(request, pk):
    """Deleta um aluguel"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        id_aluguel = aluguel.id_aluguel
        carro = aluguel.carro
        
        # Se era um aluguel ativo, liberar o carro
        if aluguel.status == 'ativo':
            carro.status = 'disponivel'
            carro.save()
        
        aluguel.delete()
        messages.success(request, f'Aluguel #{id_aluguel} deletado com sucesso!')
        return redirect('aluguel_list')
    
    return render(request, 'aluguel/aluguel_confirm_delete.html', {'aluguel': aluguel})


@cliente_required
def aluguel_detail(request, pk):
    """Exibe detalhes de um aluguel (CLIENTE e FUNCIONÁRIO)"""
    aluguel = get_object_or_404(
        Aluguel.objects.select_related('carro', 'perfil_cliente', 'funcionario'),
        pk=pk
    )
    
    # Verificar se é o cliente dono do aluguel ou funcionário
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    # Cliente só vê seus próprios aluguéis
    if not usuario.is_staff:
        try:
            perfil = PerfilCliente.objects.get(usuario=usuario)
            if aluguel.perfil_cliente != perfil:
                messages.error(request, 'Você não tem permissão para ver este aluguel!')
                return redirect('dashboard_cliente')
        except PerfilCliente.DoesNotExist:
            messages.error(request, 'Perfil não encontrado!')
            return redirect('dashboard_cliente')
    
    context = {
        'aluguel': aluguel,
    }
    
    return render(request, 'aluguel/aluguel_detail.html', context)


@staff_required
def aluguel_change_status(request, pk):
    """Altera o status do aluguel"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        
        if novo_status in ['ativo', 'finalizado', 'cancelado']:
            aluguel.status = novo_status
            aluguel.save()
            
            messages.success(request, f'Status do aluguel #{aluguel.id_aluguel} atualizado!')
        
        return redirect('aluguel_detail', pk=aluguel.pk)
    
    return redirect('aluguel_list')


@staff_required
def aluguel_finalizar(request, pk):
    """Finaliza um aluguel ativo"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        if aluguel.status == 'ativo':
            aluguel.status = 'finalizado'
            aluguel.save()
            messages.success(request, f'Aluguel #{aluguel.id_aluguel} finalizado com sucesso!')
        else:
            messages.warning(request, 'Este aluguel não está ativo!')
        
        return redirect('aluguel_detail', pk=aluguel.pk)
    
    return render(request, 'aluguel/aluguel_finalizar.html', {'aluguel': aluguel})


@staff_required
def aluguel_cancelar(request, pk):
    """Cancela um aluguel"""
    aluguel = get_object_or_404(Aluguel, pk=pk)
    
    if request.method == 'POST':
        if aluguel.status == 'ativo':
            aluguel.status = 'cancelado'
            aluguel.save()
            messages.warning(request, f'Aluguel #{aluguel.id_aluguel} cancelado!')
        else:
            messages.warning(request, 'Este aluguel não está ativo!')
        
        return redirect('aluguel_detail', pk=aluguel.pk)
    
    return render(request, 'aluguel/aluguel_cancelar.html', {'aluguel': aluguel})
    if request.method == 'POST':
        if aluguel.status == 'ativo':
            aluguel.status = 'cancelado'
            aluguel.save()
            messages.warning(request, f'Aluguel #{aluguel.id_aluguel} cancelado!')
        else:
            messages.warning(request, 'Este aluguel não está ativo!')
        
        return redirect('aluguel_detail', pk=aluguel.pk)
    
    return render(request, 'aluguel/aluguel_cancelar.html', {'aluguel': aluguel})

# ADICIONE estas views no aluguel/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Aluguel, SolicitacaoAluguel, Pagamento
from .forms import AluguelForm, SolicitacaoAluguelForm
from carro.models import Carro
from user.models import PerfilCliente, Usuario
from user.decorators import staff_required, cliente_required

@staff_required
def aprovar_solicitacao(request, pk):
    """Funcionário aprova solicitação e cria aluguel + pagamento"""
    solicitacao = get_object_or_404(SolicitacaoAluguel, pk=pk)
    
    if solicitacao.status != 'pendente':
        messages.error(request, 'Esta solicitação não está mais pendente!')
        return redirect('solicitacoes_pendentes')
    
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        funcionario = get_object_or_404(Usuario, id_usuario=user_id)
        
        # Criar o aluguel oficial
        aluguel = Aluguel.objects.create(
            perfil_cliente=solicitacao.perfil_cliente,
            carro=solicitacao.carro,
            funcionario=funcionario,
            data_inicio=solicitacao.data_inicio,
            data_fim=solicitacao.data_fim,
            valor=solicitacao.valor_estimado,
            status='ativo'
        )
        
        # Atualizar solicitação
        solicitacao.status = 'aprovado'
        solicitacao.aluguel_criado = aluguel
        solicitacao.save()
        
        # Criar pagamento
        pagamento = Pagamento.objects.create(
            aluguel=aluguel,
            valor=solicitacao.valor_estimado,
            data_vencimento=timezone.now() + timedelta(days=3),  # 3 dias para pagar
            chave_pix='louercar@pix.com',  # Configure sua chave PIX
            qr_code_pix='00020126580014BR.GOV.BCB.PIX...',  # QR Code gerado
        )
        
        # Enviar email de notificação
        try:
            pagamento.enviar_email_pagamento_pendente()
            messages.success(
                request, 
                f'✅ Solicitação aprovada! Aluguel #{aluguel.id_aluguel} criado. Email enviado ao cliente.'
            )
        except:
            messages.success(
                request, 
                f'✅ Solicitação aprovada! Aluguel #{aluguel.id_aluguel} criado. (Email não enviado - configure SMTP)'
            )
        
        return redirect('solicitacoes_pendentes')
    
    return render(request, 'aluguel/aprovar_solicitacao.html', {
        'solicitacao': solicitacao
    })


@cliente_required
def meu_pagamento(request, solicitacao_id):
    """Cliente visualiza detalhes do pagamento"""
    user_id = request.session.get('user_id')
    usuario = get_object_or_404(Usuario, id_usuario=user_id)
    
    try:
        perfil = PerfilCliente.objects.get(usuario=usuario)
        solicitacao = get_object_or_404(
            SolicitacaoAluguel,
            pk=solicitacao_id,
            perfil_cliente=perfil
        )
    except PerfilCliente.DoesNotExist:
        messages.error(request, 'Perfil não encontrado!')
        return redirect('dashboard_cliente')
    
    if not solicitacao.aluguel_criado:
        messages.error(request, 'Esta solicitação ainda não foi aprovada!')
        return redirect('minhas_solicitacoes')
    
    if not hasattr(solicitacao.aluguel_criado, 'pagamento'):
        messages.error(request, 'Pagamento não encontrado!')
        return redirect('minhas_solicitacoes')
    
    pagamento = solicitacao.aluguel_criado.pagamento
    
    return render(request, 'aluguel/meu_pagamento.html', {
        'solicitacao': solicitacao,
        'pagamento': pagamento,
        'aluguel': solicitacao.aluguel_criado,
    })


@staff_required
def confirmar_pagamento(request, pagamento_id):
    """Funcionário confirma recebimento do pagamento"""
    pagamento = get_object_or_404(Pagamento, pk=pagamento_id)
    
    if request.method == 'POST':
        pagamento.status = 'aprovado'
        pagamento.data_pagamento = timezone.now()
        pagamento.save()
        
        # Enviar email de confirmação
        try:
            pagamento.enviar_email_pagamento_aprovado()
            messages.success(request, '✅ Pagamento confirmado! Email enviado ao cliente.')
        except:
            messages.success(request, '✅ Pagamento confirmado! (Email não enviado - configure SMTP)')
        
        return redirect('aluguel_list')
    
    return render(request, 'aluguel/confirmar_pagamento.html', {
        'pagamento': pagamento
    })


@staff_required
def pagamentos_pendentes(request):
    """Lista todos os pagamentos pendentes"""
    pagamentos = Pagamento.objects.filter(
        status='pendente'
    ).select_related('aluguel', 'aluguel__perfil_cliente', 'aluguel__carro').order_by('-criado_em')
    
    context = {
        'pagamentos': pagamentos,
    }
    
    return render(request, 'aluguel/pagamentos_pendentes.html', context)