from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@stringfilter
def price_value(price):
    prefix = len(price) % 3
    return (price[0:prefix] + ' ' if prefix != 0 else '') + \
        ' '.join([price[i:i + 3] for i in range(prefix, len(price), 3)])


register.filter('price_value', price_value)
