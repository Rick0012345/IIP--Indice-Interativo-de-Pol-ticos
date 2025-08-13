from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Divide uma string usando o separador especificado"""
    return value.split(arg)

@register.filter
def get_initials(name):
    """Extrai as iniciais do nome (primeira letra + última palavra)"""
    if not name:
        return 'P'
    
    words = name.strip().split()
    if len(words) == 1:
        return words[0][:1].upper()
    
    return (words[0][:1] + words[-1][:1]).upper()