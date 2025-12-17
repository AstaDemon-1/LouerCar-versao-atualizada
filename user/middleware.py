from django.shortcuts import redirect

class AuthMiddleware:
    """Middleware para verificar autenticação em todas as páginas"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # URLs públicas (não precisam de login)
        public_paths = [
            '/',                    # Home
            '/login/',             # Login
            '/cadastro/',          # Registro
            '/logout/',            # Logout (precisa ser público para deslogar)
            '/admin/',             # Django Admin
            '/static/',            # Arquivos CSS/JS
            '/media/',             # Arquivos de mídia
        ]
        
        # Verificar se a URL atual é pública
        path = request.path
        is_public = any(path.startswith(url) for url in public_paths)
        
        # Se não for pública e não estiver logado, redireciona para LOGIN
        if not is_public and not request.session.get('user_id'):
            return redirect('login')
        
        # Adicionar usuário ao request
        if request.session.get('user_id'):
            from .models import Usuario
            try:
                request.user_obj = Usuario.objects.get(id_usuario=request.session.get('user_id'))
            except Usuario.DoesNotExist:
                # Sessão inválida - limpar e redirecionar
                request.session.flush()
                return redirect('login')
        else:
            request.user_obj = None
        
        response = self.get_response(request)
        return response