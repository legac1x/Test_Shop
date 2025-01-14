from django import template

register = template.Library()

@register.filter(name='pluralize_ru')
def pluralize_russia(value, arg):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return f"0 {arg+ 'ов'}"
    if 11 <= value % 100 <= 14:
        return f"{value} {arg + 'ов'}"
    elif value % 10 == 1:
        return f"{value} {arg}"
    elif 2 <= value % 10 <= 4:
        return f"{value} {arg + 'а'}"
    else:
        return f"{value} {arg + 'ов'}"
