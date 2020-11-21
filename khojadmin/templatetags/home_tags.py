from django import template

register = template.Library()

@register.filter(name='private')
def private(obj, attribute):
    print(obj,attribute)
    return obj[attribute]

@register.filter(name='least_desc')
def least_desc(obj, attribute):
    print(obj,attribute)
    return obj[attribute][:30]
