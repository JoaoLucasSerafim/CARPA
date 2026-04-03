from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from functools import wraps
from carpa.models import PerfilAgricultor, PerfilTecnico
from carpa.forms import FormCadastroAgricultor, FormEditarPerfilAgricultor

# ============================================================================
# DECORATORS DE PROTECAO DE ACESSO
# ============================================================================

def requer_agricultor(view_func):
    """
    Decorator que restringe acesso apenas a usuários autenticados
    com perfil de agricultor.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')

        if not hasattr(request.user, 'perfil_agricultor'):
            messages.error(request, 'Acesso negado. Esta página é exclusiva para agricultores.')
            return redirect('inicio')

        return view_func(request, *args, **kwargs)
    return wrapper

def requer_tecnico(view_func):
    """
    Decorator que restringe acesso apenas a usuários autenticados
    com perfil de técnico.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')

        if not hasattr(request.user, 'perfil_tecnico'):
            messages.error(request, 'Acesso negado. Esta página é exclusiva para técnicos.')
            return redirect('inicio')

        return view_func(request, *args, **kwargs)
    return wrapper

# ============================================================================
# VIEWS PUBLICAS
# ============================================================================

def pagina_inicial(request):
    """
    Página inicial do CARPAPA.
    """
    return render(request, "homepage/homepage.html")

def login_view(request):
    """
    View de login para agricultores e técnicos.
    """
    if request.user.is_authenticated:
        # Redirecionar usuário já logado para dashboard apropriado
        if hasattr(request.user, 'perfil_agricultor'):
            return redirect('dashboard_agricultor')
        elif hasattr(request.user, 'perfil_tecnico'):
            return redirect('dashboard_tecnico')
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Preencha todos os campos.')
            return render(request, "login/login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.get_full_name() or user.username}!')

            # Redirecionar para dashboard apropriado
            if hasattr(user, 'perfil_agricultor'):
                return redirect('dashboard_agricultor')
            elif hasattr(user, 'perfil_tecnico'):
                return redirect('dashboard_tecnico')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, "login/login.html")

def logout_view(request):
    """
    View para fazer logout.
    """
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('login')

def cadastro_agricultor(request):
    """
    View de cadastro para novos agricultores.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_agricultor')

    if request.method == 'POST':
        form = FormCadastroAgricultor(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Criar usuário
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1'],
                    first_name=form.cleaned_data['nome_completo'].split()[0],
                    last_name=' '.join(form.cleaned_data['nome_completo'].split()[1:]) if len(form.cleaned_data['nome_completo'].split()) > 1 else '',
                )

                # Criar perfil agricultor
                perfil = PerfilAgricultor.objects.create(
                    usuario=user,
                    nome_completo=form.cleaned_data['nome_completo'],
                    cpf=form.cleaned_data['cpf'],
                    rg=form.cleaned_data['rg'],
                    email=form.cleaned_data['email'],
                    telefone=form.cleaned_data['telefone'],
                    cep=form.cleaned_data['cep'],
                    endereco=form.cleaned_data['endereco'],
                    numero=form.cleaned_data['numero'],
                    complemento=form.cleaned_data['complemento'],
                    bairro=form.cleaned_data['bairro'],
                    cidade=form.cleaned_data['cidade'],
                    estado=form.cleaned_data['estado'],
                    nome_propriedade=form.cleaned_data['nome_propriedade'],
                    nomes_confrontantes=form.cleaned_data['nomes_confrontantes'],
                    tamanho_total_ha=form.cleaned_data['tamanho_total_ha'],
                    tamanho_reserva_legal_ha=form.cleaned_data['tamanho_reserva_legal_ha'],
                    tamanho_app_ha=form.cleaned_data['tamanho_app_ha'],
                    tamanho_area_uso_ha=form.cleaned_data['tamanho_area_uso_ha'],
                    tamanho_area_consolidada_ha=form.cleaned_data['tamanho_area_consolidada_ha'],
                    numero_corpos_hidricos=form.cleaned_data['numero_corpos_hidricos'],
                    numero_nascentes=form.cleaned_data['numero_nascentes'],
                    documento_posse=form.cleaned_data.get('documento_posse'),
                )

                # Fazer login automático
                login(request, user)
                messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.get_full_name() or user.username}!')
                return redirect('dashboard_agricultor')

            except Exception as e:
                # Se algo deu errado, deletar usuário criado (se foi criado)
                if 'user' in locals():
                    user.delete()
                messages.error(request, f'Erro ao criar conta: {str(e)}')
                return render(request, "login/criar_agro.html", {'form': form})
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = FormCadastroAgricultor()

    return render(request, "login/criar_agro.html", {'form': form})

# ============================================================================
# VIEWS AREA DO AGRICULTOR (REQUER LOGIN)
# ============================================================================

@requer_agricultor
def dashboard_agricultor(request):
    """
    Dashboard do agricultor - visualiza seu cadastro e status.
    """
    perfil = request.user.perfil_agricultor

    return render(request, "agricultor/dashboard.html", {
        'perfil': perfil
    })

@requer_agricultor
def editar_perfil_agricultor(request):
    """
    View para editar perfil/cadastro do agricultor.
    """
    perfil = request.user.perfil_agricultor

    if request.method == 'POST':
        form = FormEditarPerfilAgricultor(request.POST, request.FILES, instance=perfil)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('dashboard_agricultor')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar perfil: {str(e)}')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = FormEditarPerfilAgricultor(instance=perfil)

    return render(request, "agricultor/editar.html", {
        'form': form,
        'perfil': perfil
    })

# ============================================================================
# VIEWS AREA DO TECNICO (REQUER LOGIN COMO TECNICO)
# ============================================================================

@requer_tecnico
def dashboard_tecnico(request):
    """
    Dashboard do técnico - visualiza lista de agricultores para validação.
    """
    # Buscar agricultores com paginação e filtros
    status_filter = request.GET.get('status', '').strip()
    search_query = request.GET.get('search', '').strip()

    agricultores = PerfilAgricultor.objects.select_related('usuario', 'tecnico_responsavel').order_by('-data_cadastro')

    # Validar status_filter contra choices disponíveis
    VALID_STATUS = [choice[0] for choice in PerfilAgricultor.STATUS_CHOICES]
    if status_filter and status_filter in VALID_STATUS:
        agricultores = agricultores.filter(status=status_filter)
    elif status_filter:
        # Ignorar valores inválidos de status
        status_filter = ''

    # Limitar comprimento da busca
    search_query = search_query[:100]  # Máximo 100 caracteres
    if search_query:
        agricultores = agricultores.filter(
            nome_completo__icontains=search_query
        ) | agricultores.filter(
            cpf__icontains=search_query
        ) | agricultores.filter(
            nome_propriedade__icontains=search_query
        )

    return render(request, "tecnico/dashboard.html", {
        'agricultores': agricultores,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': VALID_STATUS,
    })

@requer_tecnico
def detalhe_agricultor(request, pk):
    """
    View para visualizar detalhes do cadastro de um agricultor.
    """
    agricultor = get_object_or_404(
        PerfilAgricultor.objects.select_related('usuario', 'tecnico_responsavel'),
        pk=pk
    )

    return render(request, "tecnico/detalhe_agricultor.html", {
        'agricultor': agricultor
    })

@requer_tecnico
def validar_cadastro(request, pk):
    """
    View para validar/aprovar/rejeitar cadastro de um agricultor.
    """
    agricultor = get_object_or_404(
        PerfilAgricultor.objects.select_related('usuario', 'tecnico_responsavel'),
        pk=pk
    )

    if request.method == 'POST':
        acao = request.POST.get('acao', '').strip()
        observacoes = request.POST.get('observacoes', '').strip()

        # Validar ação
        if acao not in ['aprovar', 'rejeitar']:
            messages.error(request, 'Ação inválida. Use "aprovar" ou "rejeitar".')
            return render(request, "tecnico/validar_cadastro.html", {
                'agricultor': agricultor
            })
        
        # Validar comprimento das observações
        if len(observacoes) > 1000:
            messages.error(request, 'Observações muito longas. Máximo 1000 caracteres.')
            return render(request, "tecnico/validar_cadastro.html", {
                'agricultor': agricultor
            })

        try:
            # Atualizar status
            if acao == 'aprovar':
                agricultor.status = 'aprovado'
                messages.success(request, f'✓ Cadastro de {agricultor.nome_completo} aprovado com sucesso!')
            else:  # rejeitar
                agricultor.status = 'rejeitado'
                messages.warning(request, f'✗ Cadastro de {agricultor.nome_completo} rejeitado.')

            # Atribuir técnico responsável
            agricultor.tecnico_responsavel = request.user.perfil_tecnico
            agricultor.observacoes_tecnico = observacoes
            agricultor.data_validacao = timezone.now()
            agricultor.save()

            return redirect('dashboard_tecnico')

        except Exception as e:
            messages.error(request, f'Erro ao processar validação: {str(e)}')
            return render(request, "tecnico/validar_cadastro.html", {
                'agricultor': agricultor
            })

    return render(request, "tecnico/validar_cadastro.html", {
        'agricultor': agricultor
    })