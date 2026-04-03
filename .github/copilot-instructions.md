# GitHub Copilot — Instruções para o Projeto CARPAPA

## 🌿 Visão Geral do Projeto

**CARPAPA** (Cadastro Ambiental Rural Popular Avançado do Pará) é uma aplicação web Django/Python
que democratiza o acesso ao Cadastro Ambiental Rural (CAR) para pequenos agricultores do Pará.
O objetivo é que agricultores consigam iniciar e acompanhar seu cadastro sem depender de
empresas ou engenheiros externos. Um técnico do governo do Pará valida e confirma os dados
inseridos pelos agricultores.

Repositório de referência: https://github.com/JoaoLucasSerafim/CARPA

---

## 🛠️ Stack e Ferramentas

- **Framework**: Django (Python 3.x)
- **Banco de dados**: SQLite (padrão do Django — `db.sqlite3`, sem configuração extra)
- **Validação de dados brasileiros**: `brutils` (`pip install brutils`)
- **Acessibilidade**: VLibras (widget CDN do governo federal)
- **Frontend**: HTML semântico, CSS mobile-first, sem frameworks JS externos
- **Futuro**: o app Django será convertido em APK Android (via WebView ou similar)

---

## 📁 Estrutura de Apps Django

O projeto possui dois apps principais:

### App `Login`
Gerencia autenticação e cadastro de usuários.

### App `CARPA`
Gerencia o cadastro ambiental rural em si (propriedades, validação técnica, etc.).

---

## 👤 Tipos de Usuário e Regras de Acesso

### Agricultor
- Pode **criar conta** pelo próprio site preenchendo formulário com dados pessoais e geoespaciais.
- Pode **fazer login** com usuário + senha.
- Pode visualizar e editar seus próprios dados enquanto não aprovados.
- **Não** pode acessar dados de outros agricultores.

### Técnico
- **Não pode criar conta pelo site.** Conta criada exclusivamente pelo `admin` Django
  (superusuário / dono do código).
- Pode **fazer login** com usuário + senha.
- Pode visualizar e aprovar/confirmar cadastros de agricultores.
- Tem acesso à listagem de todos os agricultores cadastrados.

### Regra de separação
Use um campo `tipo_usuario` no modelo de perfil (ou grupos Django) para distinguir
`agricultor` de `tecnico`. Nunca exponha a área de técnicos a agricultores, e vice-versa.

---

## 🗃️ Modelos Django (models.py)

### `PerfilAgricultor` (vinculado ao `User` do Django via `OneToOneField`)

```python
from django.db import models
from django.contrib.auth.models import User

class PerfilAgricultor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_agricultor')

    # Dados pessoais
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)         # "000.000.000-00"
    rg = models.CharField(max_length=30)
    cep = models.CharField(max_length=9)                        # "00000-000"
    endereco = models.TextField()

    # Documento
    documento_posse = models.FileField(upload_to='documentos/', blank=True, null=True)

    # Dados da propriedade/posse
    nome_propriedade = models.CharField(max_length=255)
    nomes_confrontantes = models.TextField(help_text="Nomes dos vizinhos/confrontantes separados por virgula")
    tamanho_total_ha = models.DecimalField(max_digits=10, decimal_places=4)
    tamanho_reserva_legal_ha = models.DecimalField(max_digits=10, decimal_places=4)
    tamanho_app_ha = models.DecimalField(max_digits=10, decimal_places=4)
    tamanho_area_uso_ha = models.DecimalField(max_digits=10, decimal_places=4)
    tamanho_area_consolidada_ha = models.DecimalField(max_digits=10, decimal_places=4)

    # Dados geoespaciais
    numero_corpos_hidricos = models.PositiveIntegerField(default=0, help_text="Rios, igarapes e corregos")
    numero_nascentes = models.PositiveIntegerField(default=0)

    # Status de validacao
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Analise'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    tecnico_responsavel = models.ForeignKey(
        'PerfilTecnico', on_delete=models.SET_NULL, null=True, blank=True
    )
    observacoes_tecnico = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_completo} — CPF: {self.cpf}"


class PerfilTecnico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_tecnico')
    matricula = models.CharField(max_length=50, unique=True)
    setor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Tecnico: {self.usuario.get_full_name()}"
```

---

## ✅ Validação com `brutils`

**Sempre use `brutils` para validar dados brasileiros.** Nunca implemente validação manual de CPF ou CEP.

### Instalação
```
pip install brutils
```

### Uso obrigatório nas views e forms:

```python
from brutils.cpf import is_valid as is_valid_cpf, remove_symbols as remove_symbols_cpf
from brutils.cep import is_valid as is_valid_cep, get_address_from_cep
from brutils.phone import is_valid as is_valid_phone
from brutils.email import is_valid as is_valid_email_br

# Exemplo de uso em clean de formulário Django
def clean_cpf(self):
    cpf_raw = self.cleaned_data.get('cpf', '')
    cpf = remove_symbols_cpf(cpf_raw)
    if not is_valid_cpf(cpf):
        raise forms.ValidationError("CPF invalido. Verifique os digitos informados.")
    return cpf_raw  # salvar formatado

def clean_cep(self):
    cep = self.cleaned_data.get('cep', '').replace('-', '')
    if not is_valid_cep(cep):
        raise forms.ValidationError("CEP invalido.")
    return self.cleaned_data.get('cep')
```

### Campos a validar com brutils:
| Campo     | Funcao brutils                        |
|-----------|---------------------------------------|
| CPF       | `brutils.cpf.is_valid`                |
| CEP       | `brutils.cep.is_valid`                |
| Email     | `brutils.email.is_valid`              |
| Telefone  | `brutils.phone.is_valid`              |

**Ao validar CEP, use `get_address_from_cep` para auto-preencher endereco via AJAX ou na view.**

---

## ♿ Integracao do VLibras

Todo template base (`base.html`) DEVE conter o widget do VLibras para acessibilidade em Libras.
Inclua **sempre** antes do fechamento do `</body>`:

```html
<!-- VLibras - Acessibilidade em Libras -->
<div vw class="enabled">
    <div vw-access-button class="active"></div>
    <div vw-plugin-wrapper>
        <div class="vw-plugin-top-wrapper"></div>
    </div>
</div>
<script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
<script>
    new window.VLibras.Widget('https://vlibras.gov.br/app');
</script>
```

---

## 🎨 Design e Visual

### Identidade Visual
- **Cores principais**: Branco (`#FFFFFF`) e Verde (`#2E7D32`)
- **Fonte**: sans-serif padrao do sistema (sem dependencias externas para funcionar offline)
- **Tom**: simples, direto, acessivel para pessoas com baixo letramento digital

### HTML Semantico Obrigatorio
Use sempre as tags corretas:
- `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- `<label for="...">` vinculado a cada `<input>` pelo `id`
- `<form>` com `action` e `method` corretos
- `<button type="submit">` para acoes de envio
- Atributos `aria-label` e `alt` em imagens

### CSS Mobile-First
O CSS deve funcionar bem em celulares primeiro, e adaptar para desktop.
```css
:root {
    --verde-principal: #2E7D32;
    --verde-claro: #4CAF50;
    --branco: #FFFFFF;
    --cinza-fundo: #F5F5F5;
    --texto-escuro: #212121;
    --borda: #C8E6C9;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    background-color: var(--cinza-fundo);
    color: var(--texto-escuro);
    font-size: 16px;
    line-height: 1.6;
}

.container {
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
    padding: 1rem;
}

input, select, textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1.5px solid var(--borda);
    border-radius: 6px;
    font-size: 1rem;
    margin-top: 0.25rem;
    margin-bottom: 1rem;
}

button[type="submit"], .btn-principal {
    background-color: var(--verde-principal);
    color: var(--branco);
    border: none;
    padding: 0.85rem 1.5rem;
    font-size: 1rem;
    border-radius: 6px;
    cursor: pointer;
    width: 100%;
}

button[type="submit"]:hover {
    background-color: var(--verde-claro);
}

@media (min-width: 768px) {
    button[type="submit"], .btn-principal {
        width: auto;
    }
}
```

---

## 🔐 Autenticacao e Views Principais

### URLs esperadas

```python
# urls.py
urlpatterns = [
    path('', views.pagina_inicial, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/agricultor/', views.cadastro_agricultor, name='cadastro_agricultor'),

    # Area do Agricultor (requer login como agricultor)
    path('agricultor/dashboard/', views.dashboard_agricultor, name='dashboard_agricultor'),
    path('agricultor/editar/', views.editar_perfil_agricultor, name='editar_perfil_agricultor'),

    # Area do Tecnico (requer login como tecnico)
    path('tecnico/dashboard/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('tecnico/agricultor/<int:pk>/', views.detalhe_agricultor, name='detalhe_agricultor'),
    path('tecnico/agricultor/<int:pk>/validar/', views.validar_cadastro, name='validar_cadastro'),
]
```

### Decorators de protecao de acesso

```python
from functools import wraps
from django.shortcuts import redirect

def requer_agricultor(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'perfil_agricultor'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def requer_tecnico(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'perfil_tecnico'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
```

---

## 📋 Formularios (forms.py)

```python
from django import forms
from brutils.cpf import is_valid as is_valid_cpf, remove_symbols as remove_symbols_cpf
from brutils.cep import is_valid as is_valid_cep

class FormCadastroAgricultor(forms.Form):
    # Dados pessoais
    nome_completo = forms.CharField(max_length=255, label="Nome Completo")
    cpf = forms.CharField(max_length=14, label="CPF")
    rg = forms.CharField(max_length=30, label="RG")
    cep = forms.CharField(max_length=9, label="CEP")
    endereco = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Endereco Completo")

    # Dados da propriedade
    nome_propriedade = forms.CharField(max_length=255, label="Nome da Posse ou Propriedade")
    nomes_confrontantes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Nomes dos Confrontantes (Vizinhos)",
        help_text="Separe os nomes por virgula"
    )
    tamanho_total_ha = forms.DecimalField(
        max_digits=10, decimal_places=4, label="Tamanho Total da Area (ha)"
    )
    tamanho_reserva_legal_ha = forms.DecimalField(
        max_digits=10, decimal_places=4, label="Tamanho da Reserva Legal (ha)"
    )
    tamanho_app_ha = forms.DecimalField(
        max_digits=10, decimal_places=4, label="Tamanho da APP (ha)"
    )
    tamanho_area_uso_ha = forms.DecimalField(
        max_digits=10, decimal_places=4, label="Tamanho da Area de Uso (ha)"
    )
    tamanho_area_consolidada_ha = forms.DecimalField(
        max_digits=10, decimal_places=4, label="Tamanho da Area Consolidada (ha)"
    )
    numero_corpos_hidricos = forms.IntegerField(
        min_value=0, label="Numero de Corpos Hidricos",
        help_text="Rios, Igarapes e Corregos"
    )
    numero_nascentes = forms.IntegerField(min_value=0, label="Numero de Nascentes")
    documento_posse = forms.FileField(label="Documento de Posse ou Propriedade", required=False)

    # Credenciais
    username = forms.CharField(max_length=150, label="Nome de Usuario")
    email = forms.EmailField(label="E-mail")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirme a Senha")

    def clean_cpf(self):
        cpf_raw = self.cleaned_data.get('cpf', '')
        cpf_limpo = remove_symbols_cpf(cpf_raw)
        if not is_valid_cpf(cpf_limpo):
            raise forms.ValidationError("CPF invalido. Verifique os digitos informados.")
        return cpf_raw

    def clean_cep(self):
        cep = self.cleaned_data.get('cep', '').replace('-', '')
        if not is_valid_cep(cep):
            raise forms.ValidationError("CEP invalido.")
        return self.cleaned_data.get('cep')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "As senhas nao coincidem.")
        return cleaned_data
```

---

## 🔧 Configuracao do `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Belem'
USE_I18N = True
USE_TZ = True

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
```

---

## 📄 Template Base (`base.html`)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="CARPAPA - Cadastro Ambiental Rural Popular Avancado do Para">
    <title>{% block titulo %}CARPAPA{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
    {% block extra_head %}{% endblock %}
</head>
<body>

<header>
    <nav aria-label="Navegacao principal">
        <a href="{% url 'inicio' %}" class="logo">🌿 CARPAPA</a>
        <ul>
            {% if user.is_authenticated %}
                {% if user.perfil_agricultor %}
                    <li><a href="{% url 'dashboard_agricultor' %}">Meu Cadastro</a></li>
                {% elif user.perfil_tecnico %}
                    <li><a href="{% url 'dashboard_tecnico' %}">Painel Tecnico</a></li>
                {% endif %}
                <li>
                    <form method="post" action="{% url 'logout' %}">
                        {% csrf_token %}
                        <button type="submit" class="btn-link">Sair</button>
                    </form>
                </li>
            {% else %}
                <li><a href="{% url 'login' %}">Entrar</a></li>
                <li><a href="{% url 'cadastro_agricultor' %}">Criar Conta</a></li>
            {% endif %}
        </ul>
    </nav>
</header>

<main>
    {% if messages %}
        <section aria-live="polite" class="mensagens">
            {% for message in messages %}
                <p class="mensagem mensagem--{{ message.tags }}">{{ message }}</p>
            {% endfor %}
        </section>
    {% endif %}

    {% block conteudo %}{% endblock %}
</main>

<footer>
    <p>CARPAPA — Cadastro Ambiental Rural Popular Avancado do Para</p>
    <p>Ferramenta complementar ao CAR oficial do SICAR.</p>
</footer>

<!-- VLibras - Acessibilidade em Libras (obrigatorio em todas as paginas) -->
<div vw class="enabled">
    <div vw-access-button class="active"></div>
    <div vw-plugin-wrapper>
        <div class="vw-plugin-top-wrapper"></div>
    </div>
</div>
<script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
<script>
    new window.VLibras.Widget('https://vlibras.gov.br/app');
</script>

{% block extra_scripts %}{% endblock %}
</body>
</html>
```

---

## ⚙️ Admin Django (`admin.py`)

```python
from django.contrib import admin
from .models import PerfilAgricultor, PerfilTecnico

@admin.register(PerfilAgricultor)
class PerfilAgricultorAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'nome_propriedade', 'status', 'data_cadastro')
    list_filter = ('status',)
    search_fields = ('nome_completo', 'cpf', 'nome_propriedade')
    readonly_fields = ('data_cadastro', 'data_atualizacao')

@admin.register(PerfilTecnico)
class PerfilTecnicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'matricula', 'setor')
    search_fields = ('usuario__username', 'matricula')
```

---

## 🚫 Regras de Codigo (Sem Bugs)

1. **Nunca deixe views sem verificacao de autenticacao** em rotas protegidas.
2. **Todo `form.is_valid()` deve ser checado** antes de salvar qualquer dado.
3. **Use `{% csrf_token %}`** em todos os formularios POST.
4. **Nunca use `request.GET` para acoes de escrita** — sempre `POST`.
5. **Nunca exiba CPF completo** na interface — mascare como `***.***.***-XX`.
6. **Valide no backend** — nunca confie somente em validacao JavaScript.
7. **Trate excecoes** ao buscar CEP via `get_address_from_cep` (pode falhar se offline).
8. **Use `get_object_or_404`** ao buscar objetos por PK em views.
9. **Arquivos de upload** devem ser salvos em `MEDIA_ROOT` — nunca no codigo-fonte.
10. **Migracoes**: sempre rode `makemigrations` e `migrate` apos alterar modelos.

---

## 📦 requirements.txt minimo

```
Django>=4.2
brutils>=2.3.0
Pillow
```

---

## 🗺️ Fluxo Resumido

```
Agricultor acessa o site
    -> Cria conta (formulario com validacao brutils)
    -> Faz login
    -> Ve dashboard com status do cadastro (pendente / em analise / aprovado)
    -> Pode editar dados enquanto pendente

Tecnico faz login (conta criada pelo admin)
    -> Ve lista de agricultores cadastrados
    -> Abre ficha de um agricultor
    -> Analisa dados, adiciona observacoes, muda status

Admin (superusuario Django)
    -> Cria contas de tecnicos pelo painel /admin/
    -> Gerencia todos os dados pelo admin Django
```
