# 🌿 CARPAPA

**Cadastro Ambiental Rural Popular Avançado do Pará**

Ferramenta web que democratiza o acesso ao [Cadastro Ambiental Rural (CAR)](https://www.car.gov.br/) para pequenos agricultores do estado do Pará. O objetivo é que o próprio agricultor consiga iniciar e acompanhar seu cadastro sem depender de empresas ou engenheiros externos. Um técnico do governo do Pará valida e confirma os dados inseridos.

> Ferramenta complementar ao CAR do [SICAR](https://www.car.gov.br/).
> 
> Acesso em: [site](https://carpapa.azurewebsites.net/)

---

## ✨ Funcionalidades

- **Agricultor** cria sua própria conta e preenche os dados da propriedade diretamente pelo site
- **Técnico** (conta criada pelo administrador) analisa, valida e aprova os cadastros
- Validação de CPF, CEP, e-mail e telefone com a biblioteca [`brutils`](https://github.com/brazilian-utils/brutils-python)
- Upload de documento de posse/propriedade e fotos de cada área (RL, APP, Uso, Consolidada, Corpos Hídricos, Nascentes)
- Acessibilidade em Libras via [VLibras](https://vlibras.gov.br/) (widget oficial do governo federal)
- Interface mobile-first, pensada para agricultores com baixo letramento digital
- Painel administrativo completo para gestão de agricultores e técnicos

---

## 🖥️ Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3 + Django 6 |
| Banco de dados | SQLite (desenvolvimento) |
| Validação BR | [brutils](https://github.com/brazilian-utils/brutils-python) |
| Imagens | Pillow |
| Servidor | Gunicorn |
| Hospedagem | Azure App Service |
| Acessibilidade | VLibras (CDN gov.br) |
| Frontend | HTML semântico + CSS mobile-first (sem frameworks JS externos) |

---

## 👤 Tipos de Usuário

### Agricultor
- Cria conta diretamente pelo site
- Preenche dados pessoais, da propriedade e envia documentos e fotos
- Acompanha o status do cadastro: `Pendente → Em Análise → Aprovado/Rejeitado`
- Pode editar seus dados enquanto o cadastro estiver pendente
- Não acessa dados de outros agricultores

### Técnico
- **Conta criada exclusivamente pelo administrador** (painel `/admin/`)
- Visualiza a lista de todos os agricultores cadastrados
- Abre a ficha de cada agricultor, adiciona observações e altera o status
- Não pode criar conta pelo site

### Administrador
- Superusuário Django com acesso ao painel `/admin/`
- Cria e gerencia contas de técnicos
- Gerencia todos os dados do sistema

---

## 🗂️ Estrutura do Projeto

```
CARPAPA/
├── CARPA/              # App principal (cadastro ambiental, models, views, admin)
│   ├── models.py       # PerfilAgricultor, PerfilTecnico
│   ├── views.py
│   ├── admin.py
│   └── forms.py
├── Login/              # App de autenticação
│   └── views.py
├── templates/          # Templates HTML (base.html e páginas)
├── staticfiles/        # Arquivos estáticos
├── manage.py
├── requirements.txt
└── procfile            # Comando de inicialização para o Azure
```

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/JoaoLucasSerafim/CARPA.git
cd CARPA

# Crie e ative um ambiente virtual
python -m venv myvenv
source myvenv/bin/activate      # Linux/Mac
myvenv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode as migrações
python manage.py migrate

# Crie um superusuário (administrador)
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

Acesse em `http://127.0.0.1:8000`

O painel administrativo está em `http://127.0.0.1:8000/admin/`

---

## ⚙️ Variáveis de Ambiente (Produção)

Em produção no Azure, as configurações de banco de dados são controladas pela variável de ambiente `WEBSITE_SITE_NAME`, definida automaticamente pelo Azure App Service.

Configure as seguintes variáveis no painel **Configuração → Configurações do aplicativo** do Azure:

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | `False` em produção |
| `ALLOWED_HOSTS` | Domínio do App Service |

---

## 📦 requirements.txt

```
Django==6.0.3
gunicorn==25.0.0
brutils>=2.3.0
Pillow
asgiref==3.11.1
sqlparse==0.5.5
```

---

## 🌐 Deploy

O deploy é feito automaticamente no **Azure App Service** a cada push na branch `main`, via GitHub Actions (`.github/workflows/`).

O `procfile` garante que as migrações rodam automaticamente a cada deploy:

```
web: python manage.py migrate --noinput && gunicorn CARPA.wsgi
```

O banco de dados SQLite fica armazenado em `/home/db.sqlite3` no Azure, diretório persistente que **não é apagado** nos deploys.

---

## ♿ Acessibilidade

Todas as páginas incluem o widget **VLibras**, ferramenta oficial do governo federal brasileiro para tradução automática de conteúdo para Língua Brasileira de Sinais (Libras).

---

## 📋 Dados coletados do Agricultor

### Dados Pessoais
- Nome completo, CPF, RG, e-mail, telefone

### Endereço de Residência
- CEP, logradouro, número, complemento, bairro, cidade, estado

### Dados da Propriedade/Posse
- Nome da propriedade
- Cidade onde a propriedade está localizada
- Como chegar à propriedade (acesso/referências)
- Nomes dos confrontantes (vizinhos)
- Tamanho total, Reserva Legal, APP, Área de Uso e Área Consolidada (em hectares)
- Número de corpos hídricos e nascentes

### Documentação e Fotos
- Documento de posse ou propriedade
- Fotos de cada área: Reserva Legal, APP, Área de Uso, Área Consolidada, Corpos Hídricos e Nascentes

---

## 📄 Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).

---

## 🤝 Sobre o Projeto

Desenvolvido com o proposito de participar da seletiva das equipes de robótica da Escola SESI Ananindeua. Também desenvolvido como ferramenta de apoio a técnicos e agricultores do estado do Pará para auxiliar no processo de Cadastro Ambiental Rural, com foco em acessibilidade, simplicidade.
