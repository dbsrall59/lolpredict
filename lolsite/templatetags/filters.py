from django import template

register = template.Library()

@register.filter()
def ranges(count):
    return range(0, count)
