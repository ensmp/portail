# -*- coding: utf-8 -*-
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

# Rajoute des liens HTML sur les urls et les @username contenus dans un texte
@register.filter(needs_autoescape=True)
@stringfilter
def linkify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x    
    message = esc(value)
    import re    
    url_pattern = re.compile(r'(https?://[-a-zA-Z0-9+&@#/%?=~_|!:.;]*)')
    urlify = url_pattern.sub(r'<a href=\\"\1\\" target=\\"_blank\\">\1</a>', message)
    username_pattern = re.compile(r'@([A-Za-z0-9_]+)')
    usernameify = username_pattern.sub(lambda m: '<a href=\\"/people/%s/\\">%s</a>' % (m.group(1), m.group(0)), urlify)
    return mark_safe(usernameify)