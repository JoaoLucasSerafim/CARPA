from django.db import models
from django.contrib.auth.models import User


class PerfilAgricultor(models.Model):
    """
    Perfil de agricultor cadastrado no CAR.
    Vinculado ao User do Django via OneToOneField.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_agricultor'
    )

    # ====== DADOS PESSOAIS ======
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)  # "000.000.000-00"
    rg = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)  # "(XX) XXXXX-XXXX"

    # ====== ENDERECO ======
    cep = models.CharField(max_length=9)  # "00000-000"
    endereco = models.TextField()
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)

    # ====== DOCUMENTO ======
    documento_posse = models.FileField(
        upload_to='documentos/',
        blank=True,
        null=True,
        help_text="Comprovante de posse ou propriedade da terra"
    )

    # ====== DADOS DA PROPRIEDADE/POSSE ======
    # ====== DADOS DA PROPRIEDADE/POSSE ======
    nome_propriedade = models.CharField(max_length=255)
    cidade_propriedade = models.CharField(           # NOVO
        max_length=100,
        blank=True,
        help_text="Cidade onde a propriedade/posse está localizada (pode ser diferente da cidade de residência)"
    )
    acesso_propriedade = models.TextField(           # NOVO
        blank=True,
        help_text="Como chegar à propriedade: referências, estradas, ramais, distâncias"
    )
    nomes_confrontantes = models.TextField(
        help_text="Nomes dos vizinhos/confrontantes separados por vírgula"
    )
        # ====== ÁREAS EM HECTARES ======
    tamanho_total_ha = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )

    tamanho_reserva_legal_ha = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )

    tamanho_app_ha = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )

    tamanho_area_uso_ha = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )

    tamanho_area_consolidada_ha = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    # ... campos de tamanho existentes permanecem iguais ...

    # ====== FOTOS DA PROPRIEDADE ======        # NOVO — bloco inteiro
    foto_reserva_legal = models.ImageField(
        upload_to='fotos/reserva_legal/',
        blank=True, null=True,
        help_text="Foto da Reserva Legal (RL) — preferencialmente com coordenadas GPS"
    )
    foto_app = models.ImageField(
        upload_to='fotos/app/',
        blank=True, null=True,
        help_text="Foto da Área de Preservação Permanente (APP)"
    )
    foto_area_uso = models.ImageField(
        upload_to='fotos/area_uso/',
        blank=True, null=True,
        help_text="Foto da Área de Uso"
    )
    foto_area_consolidada = models.ImageField(
        upload_to='fotos/area_consolidada/',
        blank=True, null=True,
        help_text="Foto da Área Consolidada"
    )
    foto_corpos_hidricos = models.ImageField(
        upload_to='fotos/corpos_hidricos/',
        blank=True, null=True,
        help_text="Foto dos Corpos Hídricos (rios, igarapés, córregos)"
    )
    foto_nascentes = models.ImageField(
        upload_to='fotos/nascentes/',
        blank=True, null=True,
        help_text="Foto das Nascentes"
    )

    # ====== DADOS GEOESPACIAIS ======
    numero_corpos_hidricos = models.PositiveIntegerField(
        default=0,
        help_text="Número de rios, igarapés e córregos"
    )
    numero_nascentes = models.PositiveIntegerField(
        default=0,
        help_text="Número de nascentes"
    )

    # ====== STATUS E VALIDACAO ======
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )
    tecnico_responsavel = models.ForeignKey(
        'PerfilTecnico',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agricultores_analisados'
    )
    observacoes_tecnico = models.TextField(
        blank=True,
        help_text="Observações do técnico sobre a validação"
    )

    # ====== TIMESTAMPS ======
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_validacao = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Perfil de Agricultor"
        verbose_name_plural = "Perfis de Agricultores"
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.nome_completo} — CPF: {self.cpf}"


class PerfilTecnico(models.Model):
    """
    Perfil de técnico responsável pela validação de cadastros.
    Vinculado ao User do Django via OneToOneField.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_tecnico'
    )

    # ====== DADOS PROFISSIONAIS ======
    matricula = models.CharField(max_length=50, unique=True)
    setor = models.CharField(
        max_length=100,
        blank=True,
        help_text="Setor/departamento do governo do Pará"
    )
    especializacao = models.CharField(
        max_length=100,
        blank=True,
        help_text="Especialização ou área de atuação"
    )
    telefone = models.CharField(max_length=20, blank=True)
    email_profissional = models.EmailField(blank=True)

    # ====== TIMESTAMPS ======
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultimo_acesso = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Perfil de Técnico"
        verbose_name_plural = "Perfis de Técnicos"
        ordering = ['usuario__last_name']

    def __str__(self):
        nome = self.usuario.get_full_name() or self.usuario.username
        return f"Técnico: {nome} — Matrícula: {self.matricula}"
