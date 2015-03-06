from django import template
from django.conf import settings


register = template.Library()

@register.simple_tag
def min_script(script_name):
    if getattr(settings, 'DEBUG', False):
        return '<script src="/static/js/{}"></script>'.format(script_name)
    return ''

