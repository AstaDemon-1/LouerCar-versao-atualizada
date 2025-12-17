from django import forms
from .models import Usuario, PerfilCliente, Grupo, UsuarioGrupo
import re

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        help_text='Mínimo 8 caracteres, deve conter: letra maiúscula, número e símbolo'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmar Senha'
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'foto_perfil', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com/foto.jpg'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'foto_perfil': 'URL da Foto de Perfil',
            'is_active': 'Ativo',
            'is_staff': 'Funcionário',
            'is_superuser': 'Administrador',
        }
        help_texts = {
            'foto_perfil': 'Cole o link de uma imagem (opcional)',
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 8:
            raise forms.ValidationError('A senha deve ter no mínimo 8 caracteres!')
        
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('A senha deve conter pelo menos uma letra maiúscula!')
        
        if not re.search(r'\d', password):
            raise forms.ValidationError('A senha deve conter pelo menos um número!')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('A senha deve conter pelo menos um símbolo (!@#$%^&*(),.?":{}|<>)!')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem!')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UsuarioUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Nova Senha',
        required=False,
        help_text='Deixe em branco para manter a senha atual. Se alterar: mínimo 8 caracteres, letra maiúscula, número e símbolo'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmar Nova Senha',
        required=False
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'foto_perfil', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com/foto.jpg'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'foto_perfil': 'URL da Foto de Perfil',
            'is_active': 'Ativo',
            'is_staff': 'Funcionário',
            'is_superuser': 'Administrador',
        }
        help_texts = {
            'foto_perfil': 'Cole o link de uma imagem (opcional)',
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if password:  # Só valida se uma nova senha foi fornecida
            if len(password) < 8:
                raise forms.ValidationError('A senha deve ter no mínimo 8 caracteres!')
            
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError('A senha deve conter pelo menos uma letra maiúscula!')
            
            if not re.search(r'\d', password):
                raise forms.ValidationError('A senha deve conter pelo menos um número!')
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise forms.ValidationError('A senha deve conter pelo menos um símbolo (!@#$%^&*(),.?":{}|<>)!')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem!')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

from django import forms
from .models import Usuario, PerfilCliente, Grupo, UsuarioGrupo, Tag, UsuarioTag
import re

# [... código anterior de UsuarioForm e UsuarioUpdateForm ...]

class TagForm(forms.ModelForm):
    """Formulário para criar/editar Tags (apenas ADMIN)"""
    class Meta:
        model = Tag
        fields = ['nome', 'cor', 'icone', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Clientes VIP, Funcionários, etc.'
            }),
            'cor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'icone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: bi-star, bi-heart, bi-award'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da tag (opcional)'
            }),
        }
        labels = {
            'nome': 'Nome da Tag',
            'cor': 'Cor da Tag',
            'icone': 'Ícone (Bootstrap Icons)',
            'descricao': 'Descrição',
        }
        help_texts = {
            'icone': 'Ícones disponíveis em: https://icons.getbootstrap.com/',
        }


class GrupoForm(forms.ModelForm):
    """Formulário para criar/editar Grupos"""
    class Meta:
        model = Grupo
        fields = ['nome', 'descricao', 'tag', 'link_whatsapp']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Grupo VIP, Equipe Suporte'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do grupo (opcional)'
            }),
            'tag': forms.Select(attrs={
                'class': 'form-control'
            }),
            'link_whatsapp': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://chat.whatsapp.com/...'
            }),
        }
        labels = {
            'nome': 'Nome do Grupo',
            'descricao': 'Descrição',
            'tag': 'Tag do Grupo',
            'link_whatsapp': 'Link do Grupo no WhatsApp',
        }
        help_texts = {
            'tag': 'Apenas usuários com esta tag poderão ver o grupo',
            'link_whatsapp': 'Link de convite do grupo no WhatsApp (opcional)',
        }


class UsuarioTagForm(forms.ModelForm):
    """Formulário para atribuir Tags a Usuários (apenas ADMIN)"""
    class Meta:
        model = UsuarioTag
        fields = ['usuario', 'tag']
        widgets = {
            'usuario': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tag': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'usuario': 'Usuário',
            'tag': 'Tag',
        }


class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        fields = ['CNH', 'telefone', 'endereco', 'usuario']
        widgets = {
            'CNH': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'CNH': 'CNH',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
            'usuario': 'Usuário',
        }


class UsuarioGrupoForm(forms.ModelForm):
    class Meta:
        model = UsuarioGrupo
        fields = ['usuario', 'grupo']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'usuario': 'Usuário',
            'grupo': 'Grupo',
        }