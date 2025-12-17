from django import forms
from .models import Carro
from datetime import datetime

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ['modelo', 'placa', 'ano', 'status', 'preco_diaria', 'foto_url', 'descricao']
        widgets = {
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Toyota Corolla'
            }),
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: ABC-1234',
                'style': 'text-transform: uppercase;'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2023',
                'min': 1900,
                'max': datetime.now().year + 1
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'preco_diaria': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 150.00',
                'step': '0.01',
                'min': '0'
            }),
            'foto_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: https://images.unsplash.com/photo-...'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o carro: motor, câmbio, ar-condicionado, direção, etc.'
            }),
        }
        labels = {
            'modelo': 'Modelo do Carro',
            'placa': 'Placa',
            'ano': 'Ano',
            'status': 'Status',
            'preco_diaria': 'Preço do Aluguel (por dia)',
            'foto_url': 'URL da Foto do Carro',
            'descricao': 'Descrição do Carro',
        }
        help_texts = {
            'placa': 'Formato: ABC-1234 ou ABC1D234',
            'ano': f'Entre 1900 e {datetime.now().year + 1}',
            'preco_diaria': 'Valor da diária de aluguel',
            'foto_url': 'Cole a URL de uma imagem (ex: Unsplash, Pexels)',
            'descricao': 'Informações sobre o carro: motor, câmbio, etc.',
        }
    
    def clean_placa(self):
        """Converte a placa para maiúsculas e valida o formato"""
        placa = self.cleaned_data.get('placa', '').upper().strip()
        
        # Remove espaços extras
        placa = placa.replace(' ', '')
        
        # Valida tamanho
        if len(placa) < 7 or len(placa) > 8:
            raise forms.ValidationError('Placa deve ter 7 ou 8 caracteres')
        
        return placa
    
    def clean_ano(self):
        """Valida o ano do carro"""
        ano = self.cleaned_data.get('ano')
        ano_atual = datetime.now().year
        
        if ano < 1900:
            raise forms.ValidationError('Ano não pode ser anterior a 1900')
        
        if ano > ano_atual + 1:
            raise forms.ValidationError(f'Ano não pode ser superior a {ano_atual + 1}')
        
        return ano
    
    def clean_preco_diaria(self):
        """Valida o preço"""
        preco = self.cleaned_data.get('preco_diaria')
        
        if preco is not None and preco <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero!')
        
        return preco