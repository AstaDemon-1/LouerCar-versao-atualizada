# 🚗 LouerCar - Sistema de Aluguel de Veículos

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-5.2.7-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![Status](https://img.shields.io/badge/Status-Concluído-success)

Sistema completo de gerenciamento de aluguel de veículos desenvolvido com Django, permitindo controle total de usuários, veículos, solicitações de aluguel e pagamentos.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Perfis de Usuário](#perfis-de-usuário)
- [Sistema de Tags e Grupos](#sistema-de-tags-e-grupos)
- [Capturas de Tela](#capturas-de-tela)
- [Contribuindo](#contribuindo)
- [Licença](#licença)
- [Contato](#contato)

## 🎯 Sobre o Projeto

O **LouerCar** é uma plataforma web completa para gerenciamento de locadora de veículos que permite:

- **Clientes**: Visualizar catálogo, solicitar aluguéis e acompanhar pagamentos
- **Funcionários**: Aprovar solicitações, gerenciar aluguéis e confirmar pagamentos
- **Administradores**: Controle total do sistema, usuários, tags e grupos

O sistema foi desenvolvido como projeto acadêmico, demonstrando boas práticas de desenvolvimento web com Django.

## ✨ Funcionalidades

### 🔐 Sistema de Autenticação
- Cadastro de usuários com validação de senha
- Login/Logout seguro com sessões
- Middleware de autenticação customizado
- Três níveis de acesso: Cliente, Funcionário e Administrador

### 🚙 Gestão de Veículos
- CRUD completo de carros
- Upload de fotos via URL
- Controle de status (disponível, alugado, manutenção)
- Preço de diária configurável
- Catálogo público com filtros

### 📝 Sistema de Solicitações
- Clientes solicitam aluguéis
- Funcionários aprovam/rejeitam
- Cálculo automático de valores
- Histórico completo de solicitações

### 💰 Gestão de Pagamentos
- Criação automática após aprovação
- Múltiplos métodos: PIX, Boleto, Cartão, Dinheiro
- Confirmação de pagamento por funcionários
- Notificações por email

### 🏷️ Sistema de Tags e Grupos (NOVO!)
- Tags para categorização de usuários
- Grupos exclusivos baseados em tags
- Integração com WhatsApp
- Atribuição automática de tags

### 📊 Dashboards Personalizados
- Dashboard do Cliente: carros disponíveis e histórico
- Dashboard do Funcionário: estatísticas operacionais
- Painéis com métricas em tempo real

### 👤 Perfil de Usuário
- Edição de dados pessoais
- Upload de foto de perfil
- Gerenciamento de CNH e documentos
- Visualização de tags e grupos

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.13.5**
- **Django 5.2.7** - Framework web principal
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend
- **HTML5 / CSS3**
- **JavaScript** (Vanilla)
- **Bootstrap 5.3.0** - Framework CSS
- **Bootstrap Icons 1.11.0** - Ícones
- **Animate.css 4.1.1** - Animações

### Infraestrutura
- **Git / GitHub** - Controle de versão
- **Django ORM** - Mapeamento objeto-relacional
- **Django Templates** - Sistema de templates

### Ferramentas de Desenvolvimento
- **Visual Studio Code** - IDE
- **Claude.ai (Anthropic)** - Assistente de desenvolvimento
- **PlantUML** - Diagramas UML
- **MySQL Workbench** - Modelagem de dados

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

```bash
Python 3.10+
pip (gerenciador de pacotes Python)
Git
```

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/louercar.git
cd louercar
```

### 2. Crie um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install django==5.2.7
```

### 4. Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Inicialize o sistema (OPCIONAL)

```bash
python manage.py init_system
```
Este comando cria tags e grupos padrão automaticamente.

### 6. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor

```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

## ⚙️ Configuração

### Configuração de Email (SMTP)

Edite `LouerCar/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'seu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua-senha-de-app'
DEFAULT_FROM_EMAIL = 'LouerCar <seu-email@gmail.com>'
```

**Nota:** Para Gmail, use [Senhas de App](https://support.google.com/accounts/answer/185833).

### Configuração de Produção

Para produção, altere em `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['seudominio.com', 'www.seudominio.com']
SECRET_KEY = 'gere-uma-chave-secreta-forte-aqui'

# Configure banco PostgreSQL/MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'louercar_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📖 Uso

### Fluxo Básico

1. **Cliente se Cadastra**
   - Acessa `/cadastro/`
   - Preenche dados básicos
   - Recebe tags automáticas

2. **Cliente Completa Perfil**
   - Adiciona CNH, telefone e endereço
   - Necessário para solicitar aluguéis

3. **Cliente Solicita Aluguel**
   - Navega pelo catálogo em `/carros/`
   - Clica em "Alugar" em um carro disponível
   - Preenche datas e observações

4. **Funcionário Aprova**
   - Acessa `/solicitacoes-pendentes/`
   - Revisa solicitação
   - Aprova ou rejeita

5. **Pagamento Gerado**
   - Sistema cria pagamento automaticamente
   - Cliente acessa `/minhas-solicitacoes/`
   - Visualiza detalhes do pagamento

6. **Funcionário Confirma Pagamento**
   - Acessa `/pagamentos-pendentes/`
   - Confirma recebimento
   - Cliente recebe email de confirmação

### Contas Padrão (Exemplo)

```
Administrador:
- Email: admin@louercar.com
- Senha: 123

Funcionário:
- Email: func@louercar.com
- Senha: 123

Cliente:
- Email: pedro@gmail.com
- Senha: 123
```

## 📁 Estrutura do Projeto

```
LouerCar/
├── LouerCar/              # Configurações do projeto
│   ├── settings.py        # Configurações gerais
│   ├── urls.py            # URLs principais
│   └── wsgi.py            # Deploy WSGI
├── user/                  # App de usuários
│   ├── models.py          # Usuario, PerfilCliente, Tag, Grupo
│   ├── views.py           # Lógica de usuários
│   ├── forms.py           # Formulários
│   ├── decorators.py      # Decoradores de permissão
│   ├── middleware.py      # Middleware de autenticação
│   └── utils.py           # Funções auxiliares (tags automáticas)
├── carro/                 # App de carros
│   ├── models.py          # Carro
│   ├── views.py           # CRUD de carros
│   └── forms.py           # Formulários
├── aluguel/               # App de aluguéis
│   ├── models.py          # Aluguel, SolicitacaoAluguel, Pagamento
│   ├── views.py           # Lógica de aluguéis e pagamentos
│   └── forms.py           # Formulários
├── template/              # Templates HTML
│   ├── base.html          # Template base
│   ├── home.html          # Landing page
│   ├── auth/              # Login, dashboards
│   ├── user/              # Templates de usuário
│   ├── carro/             # Templates de carro
│   └── aluguel/           # Templates de aluguel
├── static/                # CSS, JS, Imagens
├── media/                 # Uploads (futuro)
├── db.sqlite3             # Banco de dados
└── manage.py              # CLI do Django
```

## 👥 Perfis de Usuário

### 🔵 Cliente
**Permissões:**
- ✅ Visualizar catálogo de carros
- ✅ Solicitar aluguéis
- ✅ Ver suas solicitações
- ✅ Visualizar pagamentos
- ✅ Acessar "Meus Grupos"
- ❌ Aprovar/Rejeitar solicitações
- ❌ Gerenciar carros
- ❌ Confirmar pagamentos

### 🟢 Funcionário
**Permissões:**
- ✅ Todas do Cliente +
- ✅ Aprovar/Rejeitar solicitações
- ✅ Gerenciar carros (CRUD)
- ✅ Gerenciar aluguéis
- ✅ Confirmar pagamentos
- ❌ Gerenciar usuários
- ❌ Criar tags/grupos

### 🔴 Administrador
**Permissões:**
- ✅ Todas do Funcionário +
- ✅ Gerenciar usuários
- ✅ Criar/Editar tags
- ✅ Criar/Editar grupos
- ✅ Atribuir tags a usuários
- ✅ Acesso total ao sistema

## 🏷️ Sistema de Tags e Grupos

### Como Funciona

1. **Administrador cria Tags**
   - Ex: "Cliente VIP", "Funcionário", "Cliente Novo"
   - Define cor e ícone

2. **Administrador cria Grupos vinculados às Tags**
   - Ex: Grupo "VIP Lounge" com tag "Cliente VIP"
   - Pode incluir link do WhatsApp

3. **Usuários recebem Tags**
   - Automaticamente no cadastro
   - Ou manualmente pelo admin

4. **Usuários veem Grupos correspondentes**
   - Em "Meus Grupos" aparecem apenas grupos de suas tags
   - Podem entrar e ser redirecionados ao WhatsApp

### Inicialização Automática

Execute para criar estrutura padrão:

```bash
python manage.py init_system
```

Cria:
- Tags: Cliente Novo, Cliente VIP, Funcionário, Administrador
- Grupos: Boas-vindas, VIP, Equipe Interna

## 📸 Capturas de Tela

### Landing Page
- Design moderno com estrelas animadas
- Catálogo de carros em destaque
- Integração com WhatsApp

### Dashboard Cliente
- Carros disponíveis
- Histórico de aluguéis
- Status de solicitações

### Dashboard Funcionário
- Estatísticas do sistema
- Métricas operacionais
- Acessos rápidos

### Sistema de Solicitações
- Fluxo completo de aprovação
- Detalhes de cada solicitação
- Integração com pagamentos

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Padrões de Código

- Siga PEP 8 para Python
- Use nomes descritivos para variáveis e funções
- Documente funções complexas
- Adicione comentários quando necessário

## 📝 Licença

Este projeto é um trabalho acadêmico desenvolvido para fins educacionais.

## 📞 Contato

**Equipe LouerCar**

- WhatsApp: (61) 99988-7766
- Email: contato@louercar.com.br
- Telefone: (61) 3333-4444

---

## 🎓 Créditos

Projeto desenvolvido como trabalho acadêmico com assistência de:
- **Claude.ai (Anthropic)** - Assistente de desenvolvimento
- **Django Documentation** - Referência técnica
- **Bootstrap** - Framework CSS

## 📚 Recursos Adicionais

### Documentação Oficial
- [Django Docs](https://docs.djangoproject.com/)
- [Bootstrap Docs](https://getbootstrap.com/docs/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

### Tutoriais Recomendados
- [Django for Beginners](https://djangoforbeginners.com/)
- [Real Python - Django](https://realpython.com/tutorials/django/)

### Hospedagem Sugerida
- **PythonAnywhere** - Gratuito para projetos pequenos
- **Heroku** - Deploy simplificado
- **AWS / DigitalOcean** - Produção escalável

---

## 🎉 Changelog

### v1.8 (16/12/2025) - Release Final
- ✅ Sistema de Tags e Grupos implementado
- ✅ Atribuição automática de tags
- ✅ Integração com WhatsApp
- ✅ Dark Mode na interface
- ✅ Perfil de usuário completo
- ✅ Sistema de pagamentos funcional
- ✅ Documentação completa

### v1.7 (14/12/2025)
- ✅ Adição de Tags e Grupos
- ✅ Middleware de autenticação

### v1.6 (13/12/2025)
- ✅ Testes integrados
- ✅ Correção de bugs

### v1.5 (12/12/2025)
- ✅ Templates com Bootstrap
- ✅ API de WhatsApp

### v1.4 (11/12/2025)
- ✅ CRUD de Aluguel
- ✅ Sistema de aprovação

### v1.3 (10/12/2025)
- ✅ CRUD de Carro
- ✅ Upload de fotos

---

<div align="center">

**⭐ Se este projeto te ajudou, deixe uma estrela! ⭐**

Desenvolvido com ❤️ pela Equipe LouerCar

</div>
