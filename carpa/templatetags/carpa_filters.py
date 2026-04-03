from django import template

register = template.Library()


@register.filter
def mascarar_cpf(cpf):
    """
    Mascara um CPF, exibindo apenas os últimos 2 dígitos.
    Entrada: 123.456.789-00
    Saída: ***.***.***.00
    """
    if not cpf:
        return ''
    
    # Remove pontuação
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    
    # Verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        return cpf  # Retorna original se format inválido
    
    # Retorna mascarado
    return f"***.***.***.{cpf_limpo[-2:]}"


@register.filter
def mascarar_email(email):
    """
    Mascara um email, exibindo apenas primeira letra e domínio.
    Entrada: joao.silva@email.com
    Saída: j***@email.com
    """
    if not email:
        return ''
    
    if '@' not in email:
        return email
    
    usuario, dominio = email.split('@')
    
    if len(usuario) <= 1:
        return email
    
    # Mostra primeira letra + asteriscos + domínio
    return f"{usuario[0]}***@{dominio}"


@register.filter
def mascarar_telefone(telefone):
    """
    Mascara um telefone, exibindo apenas últimos 4 dígitos.
    Entrada: (11) 98765-4321
    Saída: (XX) XXXX-4321
    """
    if not telefone:
        return ''
    
    # Remove pontuação
    telefone_limpo = telefone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
    
    if len(telefone_limpo) < 8:
        return telefone
    
    # Formate padrão brasileiro: (XX) XXXXX-XXXX
    ultimos_4 = telefone_limpo[-4:]
    return f"(XX) XXXX-{ultimos_4}"


@register.filter
def truncate_text(text, length=50):
    """
    Trunca texto para tamanho especificado.
    """
    if not text:
        return ''
    
    if len(text) <= length:
        return text
    
    return f"{text[:length]}..."
