# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

from django import template

register = template.Library()

@register.simple_tag
def active_menu_item(request, url):
    """
    Helper pro oznaceni aktivni polozky v menu:
    pokud je `request.META['PATH_INFO']` rovno zadanemu `url`, 
    vrati retezec ' class="active"'.
    """
    if url == '/':
        active = request.META['PATH_INFO'] == url
    else:
        active = request.META['PATH_INFO'].find(url) == 0
    if active:
        return u' class="active"'
    else:
        return u''
