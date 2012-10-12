import os.path
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from contact_form.views import contact_form
from contact_form.forms import AkismetContactForm
from translations.views import regenerate

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # apps: django-contact-form app
    url(r'^kontakt/$', contact_form, {'form_class': AkismetContactForm, 'success_url': '/kontakt/odeslano/'}, name='contact_form'),
    url(r'^kontakt/odeslano/$', direct_to_template, {'template': 'contact_form/contact_form_sent.html'}, name='contact_form_sent'),
    # comments
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/translations/translation/regenerate/$', regenerate, name='translation-regenerate'),
    (r'^admin/(.*)', admin.site.root),
    (r'^(?P<path>favicon.ico|robots.txt)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # css & spol.
        (r'^%sbluetrip/(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'bluetrip')}),
        (r'^%scss/(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'css')}),
        (r'^%scompress/(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'compress')}),
        (r'^%simg/(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'img')}),
        # obrazky do prelozenych stranek
        (r'^%simages/(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': os.path.join(settings.DOC_PATH, '_build/html/_images')}),
    )
