# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

"""
Reseni od Justin Lilly.
http://justinlilly.com/blog/2009/feb/10/better-look-comments/

Contrib aplikace pro komentare zobrazuje v adminu velmi nepekne
objekt, pro ktery se komentar vztahuje (formou nazvu modelu a jeho 
ID).

Justin chovani vychoziho adminu prevalil svou tridou, ve ktere
generuje odkaz primo na objekt.

Nadherne!
"""

from django.contrib import admin
from django.contrib.comments.models import Comment
from django.contrib.comments.admin import CommentsAdmin

admin.site.unregister(Comment)

class CommentsDisplayGenericObjectAdmin(CommentsAdmin):
    list_display = ('name', 'commented_object', 'ip_address',
                    'submit_date', 'is_public', 'is_removed')

    def commented_object(self, obj):
        myobj = obj.content_type.get_object_for_this_type(id=obj.object_pk)
        return '<a href="%s">%s</a>' % (self.commented_obj_url(myobj), myobj)
    commented_object.allow_tags=True

    def commented_obj_url(self, obj):
        # hackish, needs to actually do a reverse lookup
        return '/admin/%s/%s/%s/' % (obj._meta.app_label,
                                     obj._meta.module_name,
                                     obj.id)

admin.site.register(Comment, CommentsDisplayGenericObjectAdmin)
