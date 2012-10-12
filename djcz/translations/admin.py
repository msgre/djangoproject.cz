# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

from django.contrib import admin
from models import Translation, TranslationRole
from forms import TranslationAdminForm

class TranslationRoleInline(admin.TabularInline):
    model = TranslationRole
    extra = 1

class TranslationAdmin(admin.ModelAdmin):
    list_display = ('get_short_source_path', 'revision', 'is_actual_html', 'fp_link')
    inlines = (TranslationRoleInline, )
    form = TranslationAdminForm

    def is_actual_html(self, obj):
        rev = obj.is_actual()
        if rev[0]:
            return u'<img alt="True" src="/adminmedia/img/admin/icon-yes.gif" />'
        else:
            path = u'django%2Ftrunk%2Fdocs%2F' + obj.get_short_source_path().replace('/', '%2F') + '%40'
            url = u'http://code.djangoproject.com/changeset?new=%s&old=%s' % (path + str(rev[2]), path + str(rev[1]))
            return u'<img alt="False" src="/adminmedia/img/admin/icon-no.gif" />&nbsp;&nbsp;<a href="%s" title="Zobraz diff"> <strong>Není!</strong> %i &lt; %i</a>' % (url, rev[1], rev[2])
    is_actual_html.allow_tags = True
    is_actual_html.short_description = u'Je překlad aktuální?'

    def fp_link(self, obj):
        if obj.flat_page:
            return u'<a href="/admin/flatpages/flatpage/%i/">%s</a>' % (obj.flat_page.id, obj.flat_page.title)
        else:
            return u'&mdash;'
    fp_link.allow_tags = True
    fp_link.short_description = u'Odkaz na FlatPage'


admin.site.register(Translation, TranslationAdmin)
