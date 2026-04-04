from django import forms
from django.contrib.auth.models import User
from brutils.cpf import is_valid as is_valid_cpf, remove_symbols as remove_symbols_cpf
from brutils.cep import is_valid as is_valid_cep
from brutils.phone import is_valid as is_valid_phone
from brutils.email import is_valid as is_valid_email_br
import os
from django.core.exceptions import ValidationError

from .models import PerfilAgricultor

# Validação de arquivo
ALLOWED_FILE_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_MIME_TYPES = ['application/pdf', 'image/jpeg', 'image/png']

def validar_arquivo(arquivo):
    """Validar arquivo de upload."""
    if not arquivo:
        return
    
    # Verificar tamanho
    if arquivo.size > MAX_FILE_SIZE:
        raise ValidationError(f'Arquivo muito grande. Máximo permitido: 5MB')
    
    # Verificar extensão
    ext = os.path.splitext(arquivo.name)[1].lower()
    if ext not in ALLOWED_FILE_EXTENSIONS:
        raise ValidationError(f'Tipo de arquivo não permitido. Extensões aceitas: {', '.join(ALLOWED_FILE_EXTENSIONS)}')
    
    # Verificar MIME type
    if hasattr(arquivo, 'content_type') and arquivo.content_type not in ALLOWED_MIME_TYPES:
        raise ValidationError(f'Tipo de arquivo inválido. Use PDF ou imagens (JPG, PNG).')
    
    return arquivo


class FormCadastroAgricultor(forms.Form):
    """
    Formulário de cadastro para novos agricultores.
    Valida dados pessoais, endereço, propriedade e cria conta do usuário.
    """

    # ====== DADOS PESSOAIS ======
    nome_completo = forms.CharField(
        max_length=255,
        label="Nome Completo",
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu nome completo',
            'class': 'form-control'
        })
    )
    cpf = forms.CharField(
        max_length=14,
        label="CPF",
        widget=forms.TextInput(attrs={
            'placeholder': '000.000.000-00',
            'class': 'form-control'
        })
    )
    rg = forms.CharField(
        max_length=30,
        label="RG",
        widget=forms.TextInput(attrs={
            'placeholder': 'Número do RG',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'placeholder': 'seu@email.com',
            'class': 'form-control'
        })
    )
    telefone = forms.CharField(
        max_length=20,
        label="Telefone",
        widget=forms.TextInput(attrs={
            'placeholder': '(XX) XXXXX-XXXX',
            'class': 'form-control'
        })
    )

    # ====== ENDERECO ======
    cep = forms.CharField(
        max_length=9,
        label="CEP",
        widget=forms.TextInput(attrs={
            'placeholder': '00000-000',
            'class': 'form-control'
        })
    )
    endereco = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Rua, avenida, etc',
            'class': 'form-control'
        }),
        label="Endereço Completo"
    )
    numero = forms.CharField(
        max_length=10,
        label="Número",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Número',
            'class': 'form-control'
        })
    )
    complemento = forms.CharField(
        max_length=255,
        label="Complemento",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Apto, bloco, etc (opcional)',
            'class': 'form-control'
        })
    )
    bairro = forms.CharField(
        max_length=100,
        label="Bairro",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Bairro',
            'class': 'form-control'
        })
    )
    cidade = forms.CharField(
        max_length=100,
        label="Cidade",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Cidade',
            'class': 'form-control'
        })
    )
    estado = forms.CharField(
        max_length=2,
        label="Estado (UF)",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'PA',
            'class': 'form-control'
        })
    )

    # ====== DADOS DA PROPRIEDADE ======
    nome_propriedade = forms.CharField(
        max_length=255,
        label="Nome da Posse ou Propriedade",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome da sua propriedade',
            'class': 'form-control'
        })
    )
    nomes_confrontantes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'João da Silva, Maria Santos, ...',
            'class': 'form-control'
        }),
        label="Nomes dos Confrontantes (Vizinhos)",
        help_text="Separe os nomes por vírgula"
    )

    # ====== AREAS EM HECTARES ======
    tamanho_total_ha = forms.DecimalField(
        max_digits=10,
        decimal_places=4,
        label="Tamanho Total da Área (ha)",
        widget=forms.NumberInput(attrs={
            'placeholder': '0.0000',
            'step': '0.0001',
            'class': 'form-control'
        })
    )
    tamanho_reserva_legal_ha = forms.DecimalField(
        max_digits=10,
        decimal_places=4,
        label="Tamanho da Reserva Legal (ha)",
        widget=forms.NumberInput(attrs={
            'placeholder': '0.0000',
            'step': '0.0001',
            'class': 'form-control'
        })
    )
    tamanho_app_ha = forms.DecimalField(
        max_digits=10,
        decimal_places=4,
        label="Tamanho da APP (Área de Preservação Permanente) (ha)",
        widget=forms.NumberInput(attrs={
            'placeholder': '0.0000',
            'step': '0.0001',
            'class': 'form-control'
        })
    )
    tamanho_area_uso_ha = forms.DecimalField(
        max_digits=10,
        decimal_places=4,
        label="Tamanho da Área de Uso (ha)",
        widget=forms.NumberInput(attrs={
            'placeholder': '0.0000',
            'step': '0.0001',
            'class': 'form-control'
        })
    )
    tamanho_area_consolidada_ha = forms.DecimalField(
        max_digits=10,
        decimal_places=4,
        label="Tamanho da Área Consolidada (ha)",
        widget=forms.NumberInput(attrs={
            'placeholder': '0.0000',
            'step': '0.0001',
            'class': 'form-control'
        })
    )

    # ====== DADOS GEOESPACIAIS ======
    numero_corpos_hidricos = forms.IntegerField(
        min_value=0,
        label="Número de Corpos Hídricos",
        help_text="Rios, igarapés e córregos",
        widget=forms.NumberInput(attrs={
            'placeholder': '0',
            'min': '0',
            'class': 'form-control'
        })
    )
    numero_nascentes = forms.IntegerField(
        min_value=0,
        label="Número de Nascentes",
        widget=forms.NumberInput(attrs={
            'placeholder': '0',
            'min': '0',
            'class': 'form-control'
        })
    )

    # ====== DOCUMENTO ======
    documento_posse = forms.FileField(
        label="Documento de Posse ou Propriedade",
        required=False,
        help_text="Arquivo em PDF, JPG ou PNG (máx. 5MB)",
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.jpg,.jpeg,.png',
            'class': 'form-control'
        }),
        validators=[validar_arquivo]
    )

    # ====== CREDENCIAIS ======
    username = forms.CharField(
        max_length=150,
        label="Nome de Usuário",
        widget=forms.TextInput(attrs={
            'placeholder': 'Escolha um nome de usuário',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite uma senha',
            'class': 'form-control'
        }),
        label="Senha"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a senha',
            'class': 'form-control'
        }),
        label="Confirme a Senha"
    )

    def clean_cpf(self):
        """Validar CPF usando brutils."""
        cpf_raw = self.cleaned_data.get('cpf', '')
        cpf_limpo = remove_symbols_cpf(cpf_raw)
        
        if not is_valid_cpf(cpf_limpo):
            raise forms.ValidationError(
                "CPF inválido. Verifique os dígitos informados."
            )
        
        # Verificar se CPF já está cadastrado
        if PerfilAgricultor.objects.filter(cpf=cpf_raw).exists():
            raise forms.ValidationError(
                "Este CPF já está cadastrado no sistema."
            )
        
        return cpf_raw

    def clean_cep(self):
        """Validar CEP usando brutils."""
        cep = self.cleaned_data.get('cep', '').replace('-', '')
        
        if not is_valid_cep(cep):
            raise forms.ValidationError(
                "CEP inválido. Verifique os dígitos informados."
            )
        
        return self.cleaned_data.get('cep')

    def clean_email(self):
        """Validar email usando brutils e verificar unicidade."""
        email = self.cleaned_data.get('email', '')
        
        if not is_valid_email_br(email):
            raise forms.ValidationError(
                "E-mail inválido."
            )
        
        # Verificar se email já está cadastrado
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado no sistema."
            )
        
        return email

    def clean_telefone(self):
        """Validar telefone usando brutils."""
        telefone = self.cleaned_data.get('telefone', '')
        
        if telefone and not is_valid_phone(telefone):
            raise forms.ValidationError(
                "Número de telefone inválido. Use o formato (XX) XXXXX-XXXX"
            )
        
        return telefone

    def clean_username(self):
        """Verificar se username já existe."""
        username = self.cleaned_data.get('username', '')
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Este nome de usuário já está em uso. Escolha outro."
            )
        
        return username

    def clean(self):
        """Validações gerais do formulário."""
        cleaned_data = super().clean()
        
        # Verificar senhas
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "As senhas não coincidem.")
            
            if len(password1) < 8:
                self.add_error('password1', "A senha deve ter no mínimo 8 caracteres.")
        
        # Validar áreas (área de uso não pode ser maior que total)
        tamanho_total = cleaned_data.get('tamanho_total_ha')
        tamanho_uso = cleaned_data.get('tamanho_area_uso_ha')
        
        if tamanho_total and tamanho_uso and tamanho_uso > tamanho_total:
            self.add_error('tamanho_area_uso_ha',
                          "A área de uso não pode ser maior que a área total.")
        
        # Validar que pelo menos um tipo de área foi preenchido
        areas = [
            cleaned_data.get('tamanho_reserva_legal_ha'),
            cleaned_data.get('tamanho_app_ha'),
            cleaned_data.get('tamanho_area_uso_ha'),
            cleaned_data.get('tamanho_area_consolidada_ha'),
        ]
        
        if tamanho_total and sum(filter(None, areas)) == 0:
            raise forms.ValidationError(
                "Preencha pelo menos um tipo de área."
            )
        
        return cleaned_data


class FormEditarPerfilAgricultor(forms.ModelForm):
    """
    Formulário para editar perfil do agricultor.
    Pré-preenchido com dados existentes.
    """

    class Meta:
        model = PerfilAgricultor
        fields = [
            'nome_completo',
            'rg',
            'email',
            'telefone',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'nome_propriedade',
            'nomes_confrontantes',
            'tamanho_total_ha',
            'tamanho_reserva_legal_ha',
            'tamanho_app_ha',
            'tamanho_area_uso_ha',
            'tamanho_area_consolidada_ha',
            'numero_corpos_hidricos',
            'numero_nascentes',
            'documento_posse',
            'cidade_propriedade',
            'acesso_propriedade',
        ]

        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_propriedade': forms.TextInput(attrs={'class': 'form-control'}),
            'nomes_confrontantes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tamanho_total_ha': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'tamanho_reserva_legal_ha': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'tamanho_app_ha': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'tamanho_area_uso_ha': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'tamanho_area_consolidada_ha': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'numero_corpos_hidricos': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'numero_nascentes': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'documento_posse': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_documento_posse(self):
        """Validar documento de upload."""
        arquivo = self.cleaned_data.get('documento_posse')
        if arquivo:
            validar_arquivo(arquivo)
        return arquivo

    def clean_email(self):
        """Validar email usando brutils."""
        email = self.cleaned_data.get('email', '')
        
        if not is_valid_email_br(email):
            raise forms.ValidationError(
                "E-mail inválido."
            )
        
        # Verificar se email já está cadastrado por outro usuário
        if User.objects.filter(email=email).exclude(id=self.instance.usuario.id).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado por outro usuário."
            )
        
        return email

    def clean_telefone(self):
        """Validar telefone usando brutils."""
        telefone = self.cleaned_data.get('telefone', '')
        
        if telefone and not is_valid_phone(telefone):
            raise forms.ValidationError(
                "Número de telefone inválido. Use o formato (XX) XXXXX-XXXX"
            )
        
        return telefone

    def clean_cep(self):
        """Validar CEP usando brutils."""
        cep = self.cleaned_data.get('cep', '').replace('-', '')
        
        if not is_valid_cep(cep):
            raise forms.ValidationError(
                "CEP inválido. Verifique os dígitos informados."
            )
        
        return self.cleaned_data.get('cep')
