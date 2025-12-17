# user/management/commands/init_system.py
# CRIAR ESTA ESTRUTURA DE PASTAS:
# user/
#   management/
#     __init__.py (vazio)
#     commands/
#       __init__.py (vazio)
#       init_system.py (este arquivo)

from django.core.management.base import BaseCommand
from user.utils import criar_tags_padrao, criar_grupos_padrao

class Command(BaseCommand):
    help = 'Inicializa o sistema com tags e grupos padrão'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🚀 Iniciando sistema...'))
        
        # Criar tags
        self.stdout.write('📝 Criando tags padrão...')
        tags_criadas = criar_tags_padrao()
        if tags_criadas:
            self.stdout.write(self.style.SUCCESS(f'✅ Tags criadas: {", ".join(tags_criadas)}'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Tags já existem'))
        
        # Criar grupos
        self.stdout.write('👥 Criando grupos padrão...')
        grupos_criados = criar_grupos_padrao()
        if grupos_criados:
            self.stdout.write(self.style.SUCCESS(f'✅ Grupos criados: {", ".join(grupos_criados)}'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Grupos já existem'))
        
        self.stdout.write(self.style.SUCCESS('\n✨ Sistema inicializado com sucesso!'))
        self.stdout.write(self.style.SUCCESS('Você pode agora:'))
        self.stdout.write('  1. Cadastrar novos usuários (receberão tags automáticas)')
        self.stdout.write('  2. Gerenciar tags em: /tags/')
        self.stdout.write('  3. Gerenciar grupos em: /grupos/')
        self.stdout.write('  4. Ver "Meus Grupos" como cliente\n')