from django import template
from datetime import date


register = template.Library()

@register.filter(name='age')
def age(value, arg):
    currentmonth = int(value.month)
    currentday = int(value.day)
    monthofbirth = int(arg.month)
    dayofbirth = int(arg.day)
    currentyear = int(value.year)
    yearofbirth = int(arg.year)
    return currentyear - yearofbirth - ((currentmonth, currentday) < (monthofbirth, dayofbirth))