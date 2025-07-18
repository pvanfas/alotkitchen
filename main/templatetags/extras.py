from django import template

register = template.Library()


@register.filter
def lookup(obj, key):
    """
    Custom template filter to dynamically access object attributes
    Usage: {{ preference|lookup:"monday_breakfast_id" }}
    """
    try:
        return getattr(obj, key)
    except AttributeError:
        return None


@register.filter
def split(value, delimiter):
    """
    Split a string by delimiter
    Usage: {{ "a,b,c"|split:"," }}
    """
    return value.split(delimiter)
