from django.contrib import admin
from .models import PerfilAgricultor, PerfilTecnico


@admin.register(PerfilAgricultor)
class PerfilAgricultorAdmin(admin.ModelAdmin):
    """
    Admin customizado para PerfilAgricultor.
    """
    list_display = (
        'nome_completo',
        'cpf',
        'nome_propriedade',
        'status',
        'data_cadastro'
    )
    list_filter = ('status', 'data_cadastro', 'estado')
    search_fields = ('nome_completo', 'cpf', 'nome_propriedade', 'endereco')
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
        ('Endereço', {
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
        ('Documetação', {
            'fields': ('documento_posse',),
            'classes': ('collapse',)
        }),
        ('Dados da Propriedade', {
            'fields': (
                'nome_propriedade',
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


@admin.register(PerfilTecnico)
class PerfilTecnicoAdmin(admin.ModelAdmin):
    """
    Admin customizado para PerfilTecnico.
    """
    list_display = (
        'usuario',
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
