from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """
    Decorator para restringir acesso APENAS a ADMINISTRADORES (is_staff=True)
    Funcionários NÃO podem acessar views com este decorator
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica se está logado
        if not request.session.get('user_id'):
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('login')
        
        # Verifica se é staff (admin/funcionário)
        if not request.session.get('is_staff'):
            messages.error(request, 'Acesso negado! Apenas administradores podem acessar esta página.')
            return redirect('dashboard_cliente')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def staff_required(view_func):
    """
    Decorator para views que funcionários E administradores podem acessar
    (Carros, Aluguéis, etc)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica se está logado
        if not request.session.get('user_id'):
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('login')
        
        # Verifica se é staff
        if not request.session.get('is_staff'):
            messages.error(request, 'Acesso negado! Apenas funcionários podem acessar esta página.')
            return redirect('dashboard_cliente')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def cliente_required(view_func):
    """
    Decorator para views que QUALQUER usuário autenticado pode acessar
    (Clientes, Funcionários e Admins)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica se está logado
        if not request.session.get('user_id'):
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper