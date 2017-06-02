from urllib.parse import quote_plus
from django import template

register = template.Library()

@register.filter        #custom filter for social links ,works as builtin filter 'timesince'
def urlify(value):
    return quote_plus(value)
