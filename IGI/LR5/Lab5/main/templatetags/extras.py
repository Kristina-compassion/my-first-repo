from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    if isinstance(dictionary, (list, tuple)):
        try:
            return dictionary[key]
        except (IndexError, TypeError):
            return 0
    if hasattr(dictionary, 'keys'):
        return list(dictionary.keys())[key] if len(dictionary.keys()) > key else 0
    return 0

@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    try:
        arg = float(arg)
        if arg == 0:
            return 0
        return float(value) / arg
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0