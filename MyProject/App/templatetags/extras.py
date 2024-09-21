from django import template
from datetime import date

register = template.Library()


@register.filter(expects_localtime=True)
def is_no_deadline(value):
    today = date.today()
    return value < today

@register.filter()
def remove_colon(value):
    if type(value) is not str:
        raise
    return value.rstrip(':')

# @register.filter()
# def isN(value):
#     raise