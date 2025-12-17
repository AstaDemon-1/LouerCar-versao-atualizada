from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Carro
from .forms import CarroForm
from user.decorators import staff_required, cliente_required

@cliente_required  # Qualquer usuário pode VER carros
def carro_list(request):
    """Lista todos os carros com filtros de busca"""
    carros = Carro.objects.all()
    
    # Filtro de busca
    query = request.GET.get('q')
    if query:
        carros = carros.filter(
            Q(modelo__icontains=query) |
            Q(placa__icontains=query)
        )
    
    # Filtro por status
    status_filter = request.GET.get('status')
    if status_filter:
        carros = carros.filter(status=status_filter)
    
    # Estatísticas
    total_carros = Carro.objects.count()
    disponiveis = Carro.objects.filter(status='disponivel').count()
    alugados = Carro.objects.filter(status='alugado').count()
    manutencao = Carro.objects.filter(status='manutencao').count()
    
    context = {
        'carros': carros,
        'total_carros': total_carros,
        'disponiveis': disponiveis,
        'alugados': alugados,
        'manutencao': manutencao,
        'query': query,
        'status_filter': status_filter,
    }
    
    return render(request, 'carro/carro_list.html', context)


@staff_required  # Apenas STAFF pode criar carros
def carro_create(request):
    """Cria um novo carro"""
    if request.method == 'POST':
        form = CarroForm(request.POST)
        if form.is_valid():
            carro = form.save()
            messages.success(request, f'Carro {carro.modelo} cadastrado com sucesso!')
            return redirect('carro_list')
    else:
        form = CarroForm()
    
    return render(request, 'carro/carro_form.html', {
        'form': form,
        'title': 'Cadastrar Novo Carro'
    })


@staff_required  # Apenas STAFF pode editar carros
def carro_update(request, pk):
    """Atualiza um carro existente"""
    carro = get_object_or_404(Carro, pk=pk)
    
    if request.method == 'POST':
        form = CarroForm(request.POST, instance=carro)
        if form.is_valid():
            carro = form.save()
            messages.success(request, f'Carro {carro.modelo} atualizado com sucesso!')
            return redirect('carro_detail', pk=carro.pk)
    else:
        form = CarroForm(instance=carro)
    
    return render(request, 'carro/carro_form.html', {
        'form': form,
        'title': f'Editar {carro.modelo}',
        'carro': carro
    })


@staff_required  # Apenas STAFF pode deletar carros
def carro_delete(request, pk):
    """Deleta um carro"""
    carro = get_object_or_404(Carro, pk=pk)
    
    if request.method == 'POST':
        modelo = carro.modelo
        placa = carro.placa
        carro.delete()
        messages.success(request, f'Carro {modelo} ({placa}) deletado com sucesso!')
        return redirect('carro_list')
    
    return render(request, 'carro/carro_confirm_delete.html', {'carro': carro})


@cliente_required  # Qualquer usuário pode VER detalhes
def carro_detail(request, pk):
    """Exibe detalhes de um carro"""
    carro = get_object_or_404(Carro, pk=pk)
    
    context = {
        'carro': carro,
    }
    
    return render(request, 'carro/carro_detail.html', context)


@staff_required  # Apenas STAFF pode mudar status
def carro_change_status(request, pk):
    """Altera o status do carro"""
    carro = get_object_or_404(Carro, pk=pk)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        
        if novo_status in ['disponivel', 'alugado', 'manutencao']:
            status_antigo = carro.get_status_display()
            carro.status = novo_status
            carro.save()
            
            status_messages = {
                'disponivel': ('success', 'DISPONÍVEL'),
                'alugado': ('warning', 'ALUGADO'),
                'manutencao': ('danger', 'EM MANUTENÇÃO'),
            }
            
            msg_type, msg_status = status_messages.get(novo_status, ('info', 'ATUALIZADO'))
            
            if msg_type == 'success':
                messages.success(request, f'Carro {carro.modelo} marcado como {msg_status}')
            elif msg_type == 'warning':
                messages.warning(request, f'Carro {carro.modelo} marcado como {msg_status}')
            else:
                messages.error(request, f'Carro {carro.modelo} marcado como {msg_status}')
        
        return redirect('carro_detail', pk=carro.pk)
    
    return redirect('carro_list')