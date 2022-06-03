from django import template
register = template.Library()


def cut(value):

    """
    cuts out all values of the "arg" from the string!
    """
    return value.replace('')
# register.filter('cut',cut)
@register.filter(name='cut')
