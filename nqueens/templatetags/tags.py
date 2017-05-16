from django import template

register = template.Library()


@register.filter
def index(list, idx):
    return list[idx]