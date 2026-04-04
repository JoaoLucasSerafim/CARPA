from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import PerfilAgricultor, PerfilTecnico


# ── Inline do Técnico dentro do User ─────────────────────────────────────────

class PerfilTecnicoInline(admin.StackedInline):
    model = PerfilTecnico
    can_delete = False
    verbose_name = "Perfil de Técnico"
    verbose_name_plural = "Perfil de Técnico"
    extra = 0
    fields = ('matricula', 'setor', 'especializacao', 'telefone', 'email_profissional')


class FormCriacaoUsuarioPT(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = (
            'Obrigatório. Até 150 caracteres. '
            'Letras, números e os símbolos @, ., +, -, _ são permitidos.'
        )
        self.fields['password1'].help_text = (
            'A senha deve ter pelo menos 8 caracteres e não pode ser muito simples.'
        )
        self.fields['password2'].help_text = (
            'Digite a mesma senha novamente para confirmação.'
        )


class FormEdicaoUsuarioPT(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = (
            'Obrigatório. Até 150 caracteres. '
            'Letras, números e os símbolos @, ., +, -, _ são permitidos.'
        )


class UserAdminComTecnico(BaseUserAdmin):
    add_form = FormCriacaoUsuarioPT
    form = FormEdicaoUsuarioPT
    inlines = [PerfilTecnicoInline]


admin.site.unregister(User)
admin.site.register(User, UserAdminComTecnico)


# ── PerfilAgricultor ──────────────────────────────────────────────────────────

@admin.register(PerfilAgricultor)
class PerfilAgricultorAdmin(admin.ModelAdmin):
    """
    Admin customizado para PerfilAgricultor.
    """
    list_display = (
        'nome_completo',
        'cpf',
        'nome_propriedade',
        'cidade_propriedade',
        'status',
        'data_cadastro'
    )
    list_filter = ('status', 'data_cadastro', 'estado')
    search_fields = ('nome_completo', 'cpf', 'nome_propriedade', 'endereco', 'cidade_propriedade')
    readonly_fields = ('data_cadastro', 'data_atualizacao', 'data_validacao')

    fieldsets = (
        ('Usuário', {
            'fields': ('usuario',)
        }),
        ('Dados Pessoais', {
            'fields': (
                'nome_completo',
                'cpf',
                'rg',
                'email',
                'telefone'
            )
        }),
        ('Endereço de Residência', {
            'fields': (
                'cep',
                'endereco',
                'numero',
                'complemento',
                'bairro',
                'cidade',
                'estado'
            ),
            'classes': ('collapse',)
        }),
        ('Documentação', {
            'fields': ('documento_posse',),
            'classes': ('collapse',)
        }),
        ('Dados da Propriedade', {
            'fields': (
                'nome_propriedade',
                'cidade_propriedade',       # NOVO
                'acesso_propriedade',       # NOVO
                'nomes_confrontantes',
                'tamanho_total_ha',
                'tamanho_reserva_legal_ha',
                'tamanho_app_ha',
                'tamanho_area_uso_ha',
                'tamanho_area_consolidada_ha'
            )
        }),
        ('Dados Geoespaciais', {
            'fields': (
                'numero_corpos_hidricos',
                'numero_nascentes'
            ),
            'classes': ('collapse',)
        }),
        ('Fotos da Propriedade', {           # NOVO
            'fields': (
                'foto_reserva_legal',
                'foto_app',
                'foto_area_uso',
                'foto_area_consolidada',
                'foto_corpos_hidricos',
                'foto_nascentes'
            ),
            'classes': ('collapse',),
            'description': 'Envie fotos de cada área. Fotos tiradas com GPS ativado terão coordenadas geográficas registradas automaticamente.'
        }),
        ('Status e Validação', {
            'fields': (
                'status',
                'tecnico_responsavel',
                'observacoes_tecnico',
                'data_cadastro',
                'data_atualizacao',
                'data_validacao'
            )
        }),
    )


# ── PerfilTecnico ─────────────────────────────────────────────────────────────

@admin.register(PerfilTecnico)
class PerfilTecnicoAdmin(admin.ModelAdmin):
    """
    Admin customizado para PerfilTecnico.
    """
    list_display = (
        'get_nome',
        'matricula',
        'setor',
        'data_criacao'
    )
    list_filter = ('setor', 'data_criacao')
    search_fields = ('usuario__username', 'usuario__first_name', 'matricula', 'setor')
    readonly_fields = ('data_criacao', 'data_ultimo_acesso')

    fieldsets = (
        ('Usuário', {
            'fields': ('usuario',)
        }),
        ('Dados Profissionais', {
            'fields': (
                'matricula',
                'setor',
                'especializacao',
                'telefone',
                'email_profissional'
            )
        }),
        ('Timestamps', {
            'fields': (
                'data_criacao',
                'data_ultimo_acesso'
            ),
            'classes': ('collapse',)
        }),
    )

    def get_nome(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username
    get_nome.short_description = "Nome do Técnico"