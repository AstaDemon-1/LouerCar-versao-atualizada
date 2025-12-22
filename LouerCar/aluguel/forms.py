from django import forms
from .models import Aluguel, SolicitacaoAluguel
from carro.models import Carro
from user.models import PerfilCliente, Usuario
from django.utils import timezone

class SolicitacaoAluguelForm(forms.ModelForm):
    """
    Formulário para CLIENTE solicitar aluguel
    """
    class Meta:
        model = SolicitacaoAluguel
        fields = ['carro', 'data_inicio', 'data_fim', 'observacoes']
        widgets = {
            'carro': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'data_fim': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Alguma observação sobre o aluguel? (opcional)'
            }),
        }
        labels = {
            'carro': 'Selecione o Carro',
            'data_inicio': 'Data/Hora de Início',
            'data_fim': 'Data/Hora de Término',
            'observacoes': 'Observações (opcional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apenas carros disponíveis
        self.fields['carro'].queryset = Carro.objects.filter(status='disponivel')
        
        # Melhorar exibição dos carros
        carro_choices = []
        for carro in self.fields['carro'].queryset:
            label = f"{carro.modelo} - {carro.placa} (R$ {carro.preco_diaria}/dia)"
            carro_choices.append((carro.id_carro, label))
        self.fields['carro'].choices = [('', 'Selecione um carro...')] + carro_choices
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        carro = cleaned_data.get('carro')
        
        # Validar datas
        if data_inicio and data_fim:
            if data_fim <= data_inicio:
                raise forms.ValidationError(
                    'A data de término deve ser posterior à data de início!'
                )
            
            # Não permitir datas no passado
            if data_inicio < timezone.now():
                raise forms.ValidationError(
                    'A data de início não pode ser no passado!'
                )
        
        # Validar se o carro está disponível
        if carro and carro.status != 'disponivel':
            raise forms.ValidationError(
                f'O carro {carro.modelo} não está disponível no momento!'
            )
        
        return cleaned_data


class AluguelForm(forms.ModelForm):
    """
    Formulário para FUNCIONÁRIO criar aluguel (após aprovar solicitação)
    """
    class Meta:
        model = Aluguel
        fields = ['perfil_cliente', 'carro', 'funcionario', 'data_inicio', 'data_fim', 'valor', 'status']
        widgets = {
            'perfil_cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'carro': forms.Select(attrs={
                'class': 'form-control'
            }),
            'funcionario': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'data_fim': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ex: 150.00'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'perfil_cliente': 'Cliente',
            'carro': 'Carro',
            'funcionario': 'Funcionário Responsável',
            'data_inicio': 'Data/Hora de Início',
            'data_fim': 'Data/Hora de Término',
            'valor': 'Valor Total (R$)',
            'status': 'Status do Aluguel',
        }
        help_texts = {
            'carro': 'Apenas carros disponíveis serão listados',
            'funcionario': 'Funcionário que está registrando o aluguel',
            'valor': 'Valor total do aluguel em reais',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar apenas carros disponíveis (quando criando novo aluguel)
        if not self.instance.pk:  # Novo aluguel
            self.fields['carro'].queryset = Carro.objects.filter(status='disponivel')
        
        # Filtrar apenas funcionários (is_staff=True)
        self.fields['funcionario'].queryset = Usuario.objects.filter(is_staff=True)
        
        # Adicionar informação extra aos labels dos carros
        carro_choices = []
        for carro in self.fields['carro'].queryset:
            label = f"{carro.modelo} - {carro.placa} ({carro.ano})"
            carro_choices.append((carro.id_carro, label))
        self.fields['carro'].choices = [('', '---------')] + carro_choices
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        carro = cleaned_data.get('carro')
        
        # Validar datas
        if data_inicio and data_fim:
            if data_fim <= data_inicio:
                raise forms.ValidationError(
                    'A data de término deve ser posterior à data de início!'
                )
            
            # Não permitir datas no passado (apenas para novos aluguéis)
            if not self.instance.pk:  # Novo aluguel
                if data_inicio < timezone.now():
                    raise forms.ValidationError(
                        'A data de início não pode ser no passado!'
                    )
        
        # Validar se o carro está disponível (apenas para novos aluguéis)
        if carro and not self.instance.pk:
            if carro.status != 'disponivel':
                raise forms.ValidationError(
                    f'O carro {carro.modelo} não está disponível no momento!'
                )
        
        return cleaned_data
    
    def clean_valor(self):
        """Valida o valor do aluguel"""
        valor = self.cleaned_data.get('valor')
        
        if valor is not None and valor <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero!')
        
        return valor