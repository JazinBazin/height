from django import template
from django.template.defaultfilters import stringfilter
from math import modf

register = template.Library()


def acres_display(value):
    frac, whole = modf(value)
    if frac == 0:
        whole = whole % 10 if whole > 20 else whole
        if whole == 1:
            return 'сотка'
        elif 0 < whole < 5:
            return 'сотки'
        else:
            return 'соток'
    else:
        return 'сотки'


@stringfilter
def price_value(price):
    prefix = len(price) % 3
    return (price[0:prefix] + ' ' if prefix != 0 else '') + \
        ' '.join([price[i:i + 3] for i in range(prefix, len(price), 3)])


register.filter('price_value', price_value)
register.filter('acres_display', acres_display)
