# 🚗 LouerCar - Sistema de Aluguel de Veículos

Sistema completo de gerenciamento de locadora de veículos com **interface web responsiva** e **API RESTful**.

---

## 🌐 Acesse o Sistema Online

**🔗 Link do projeto:** ``

---

## 📋 Sobre o Projeto

**LouerCar** é uma plataforma de gerenciamento de locadora que oferece controle completo de veículos, aluguéis, solicitações e pagamentos.

### 🎯 Funcionalidades Principais

#### 👤 Cliente
- ✅ Visualizar catálogo de carros disponíveis
- ✅ Solicitar aluguéis online
- ✅ Acompanhar status de solicitações
- ✅ Visualizar informações de pagamento
- ✅ Participar de grupos exclusivos
- ✅ Perfil personalizável com foto

#### 👔 Funcionário
- ✅ Aprovar/rejeitar solicitações de aluguel
- ✅ Gerenciar carros (CRUD completo)
- ✅ Controlar aluguéis ativos
- ✅ Confirmar recebimento de pagamentos
- ✅ Dashboard com estatísticas operacionais

#### 👨‍💼 Administrador
- ✅ Controle total do sistema
- ✅ Gerenciar usuários e permissões
- ✅ Criar e atribuir tags aos usuários
- ✅ Gerenciar grupos com integração WhatsApp
- ✅ Acesso completo à API REST

---

## 🛠️ Tecnologias

### Backend
- **Python 3.13.5**
- **Django 5.2.7** - Framework web
- **Django REST Framework 3.14.0** - API RESTful
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend
- **HTML5 / CSS3 / JavaScript**
- **Bootstrap 5.3.0** - Framework CSS
- **Bootstrap Icons 1.11.0**
- **Animate.css 4.1.1**

---

## 📦 Instalação Local

### Pré-requisitos
- Python 3.10+
- pip
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/LouerCar.git
cd LouerCar
```

### 2. Crie ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Execute migrações
```bash
python manage.py migrate
```

### 5. (OPCIONAL) Inicialize sistema
```bash
python manage.py init_system
```
*Cria tags e grupos padrão*

### 6. Crie superusuário
```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor
```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

---

## 📁 Estrutura do Projeto

```
LouerCar/
├── manage.py                      # CLI do Django
├── requirements.txt               # Dependências
├── README.md                      # Este arquivo
│
├── LouerCar/                      # Configurações do projeto
│   ├── settings.py                # Configurações gerais
│   ├── urls.py                    # Rotas principais
│   └── wsgi.py                    # Deploy WSGI
│
├── api/                           # API REST Framework
│   ├── serializers.py             # Serializadores JSON
│   ├── views.py                   # ViewSets da API
│   └── urls.py                    # Rotas da API
│
├── user/                          # App de usuários
│   ├── models.py                  # Usuario, PerfilCliente, Tag, Grupo
│   ├── views.py                   # Lógica de usuários
│   ├── auth_views.py              # Login, registro, dashboards
│   └── ...
│
├── carro/                         # App de carros
│   ├── models.py                  # Modelo Carro
│   ├── views.py                   # CRUD de carros
│   └── ...
│
├── aluguel/                       # App de aluguéis
│   ├── models.py                  # Aluguel, SolicitacaoAluguel, Pagamento
│   ├── views.py                   # Lógica de aluguéis
│   └── ...
│
├── template/                      # Templates HTML
│   ├── base.html                  # Template base
│   ├── home.html                  # Landing page
│   ├── auth/                      # Login e dashboards
│   ├── user/                      # Templates de usuário
│   ├── carro/                     # Templates de carro
│   └── aluguel/                   # Templates de aluguel
│
└── static/                        # CSS, JS, Imagens
```

---

## 🔌 API REST

### Autenticação

A API usa **autenticação por sessão** do Django.

1. Faça login via interface web: `/login/`
2. Acesse a API: `/api/`

### Endpoints Principais

```
GET    /api/carros/                # Lista todos os carros
GET    /api/carros/disponiveis/    # Lista apenas disponíveis
GET    /api/alugueis/              # Lista aluguéis
GET    /api/solicitacoes/          # Lista solicitações
GET    /api/solicitacoes/pendentes/  # Pendentes (staff)
GET    /api/pagamentos/            # Lista pagamentos
GET    /api/usuarios/me/           # Seus dados
GET    /api/tags/                  # Lista tags
GET    /api/grupos/                # Lista grupos
```

### Testando a API

**Navegador:**
```
1. Login: http://localhost:8000/login/
2. API: http://localhost:8000/api/
```

**cURL:**
```bash
curl -X GET http://localhost:8000/api/carros/disponiveis/
```

---

## 👥 Perfis de Usuário

### 🔵 Cliente
- Visualizar catálogo e solicitar aluguéis
- Acompanhar solicitações e pagamentos
- Participar de grupos exclusivos

### 🟢 Funcionário
- Aprovar/rejeitar solicitações
- Gerenciar carros e aluguéis
- Confirmar pagamentos

### 🔴 Administrador
- Controle total do sistema
- Gerenciar usuários e permissões
- Acesso completo à API

---

## 🏷️ Sistema de Tags e Grupos

### Funcionamento

1. **Admin cria Tags** (ex: "Cliente VIP", "Funcionário")
2. **Admin cria Grupos** vinculados às tags
3. **Usuários recebem Tags** (automático no cadastro)
4. **Usuários veem Grupos** baseado em suas tags

### Inicialização Automática

```bash
python manage.py init_system
```

Cria tags e grupos padrão automaticamente.

---

## 🔐 Segurança

- ✅ Validação de senha forte (8+ chars, maiúscula, número, símbolo)
- ✅ Middleware de autenticação customizado
- ✅ Decoradores de permissão por nível
- ✅ Proteção CSRF em formulários
- ✅ Sessões seguras do Django

---

## 🎨 Interface

- **Light/Dark Mode** alternável pelo usuário
- Design responsivo com Bootstrap 5
- Animações suaves com Animate.css
- Landing page com estrelas animadas
- Sidebar fixa com navegação intuitiva

---

## 📝 Comandos Úteis

```bash
# Migrações
python manage.py makemigrations
python manage.py migrate

# Superusuário
python manage.py createsuperuser

# Inicializar sistema (tags e grupos)
python manage.py init_system

# Servidor local
python manage.py runserver

# Shell interativo
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic
```

---

## 🧪 Contas de Teste

```
Administrador:
- Username: admin
- Senha: 123

Funcionário:
- Username: funcionario
- Senha: 123

Cliente:
- Username: pedro
- Senha: 123
```

---

## 🚀 Deploy no PythonAnywhere

### 1. Criar conta no PythonAnywhere
```
https://www.pythonanywhere.com/
```

### 2. Clone o repositório
```bash
git clone https://github.com/seu-usuario/LouerCar.git
cd LouerCar
```

### 3. Crie ambiente virtual
```bash
mkvirtualenv --python=/usr/bin/python3.10 louercar
pip install -r requirements.txt
```

### 4. Configure o projeto
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### 5. Configure o Web App
- WSGI file: aponte para `LouerCar/wsgi.py`
- Static files: `/static/` → `/home/seu-usuario/LouerCar/staticfiles/`
- Virtual env: `/home/seu-usuario/.virtualenvs/louercar/`

### 6. Reload da aplicação
Clique em "Reload" no dashboard do PythonAnywhere

---

## 📚 Documentação

- [Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5](https://getbootstrap.com/)
- [PythonAnywhere](https://help.pythonanywhere.com/)

---

## 🎓 Informações Acadêmicas

Projeto desenvolvido como trabalho acadêmico demonstrando:

✅ Arquitetura MVC completa  
✅ API RESTful funcional  
✅ Autenticação e autorização robustas  
✅ CRUD em múltiplos modelos  
✅ Relacionamentos complexos entre modelos  
✅ Interface responsiva moderna  
✅ Boas práticas de desenvolvimento  
✅ Deploy em produção  

---

## 📞 Contato

**LouerCar**
- WhatsApp: (61) 99999-9999
- Telefone: (61) 9999-9999

---

## 📄 Licença

Projeto acadêmico para fins educacionais.

---

<div align="center">

**⭐ Desenvolvido com Django + Django REST Framework ⭐**

</div>
