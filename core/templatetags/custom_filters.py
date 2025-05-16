from django import template

register = template.Library()

@register.filter
def includes(queryset, item):
    if queryset is None:
        return False
    return item in queryset