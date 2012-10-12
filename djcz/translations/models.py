# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

"""
TODO:
testy pro manager a rewrite()
"""

import os.path
import re
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from djcz.translations.utils import doc_rewrite_if_not_same, doc_build, DocHtmlProcessor, doc_last_change_revision


class TranslationManager(models.Manager):
    DOC_CONTENT_TEMPLATE = 'translations/translation_content.html'

    def _rewrite_original_docs(self):
        """
        Prepise originalni Django soubory s dokumentaci nasimi preklady
        ulozenymi v databazi.
        """
        for obj in super(TranslationManager, self).all():
            obj.rewrite()

    def html_to_flatpage(self):
        """
        Prevede prelozene, zkompilovane HTML stranky do Flatpage:

        * prevedene do naseho layoutu
        * URL vedouci na nase preklady (pokud existuji); v opacnem pripade
          smeruji na oficialni dokumentaci
        * prelozene posledni zbytky anglickych fragmentu v tele stranky
        """
        translated_urls = [i.get_absolute_url() for i in super(TranslationManager, self).all()]
        for obj in super(TranslationManager, self).all():
            # tady se deje vse podstatne:
            dhp = DocHtmlProcessor(obj.source_html_content, obj.html_id.replace('/', '-'))
            title, _content, sidebar = dhp.process(translated_urls)
            context = {
                'content': _content,
                'sidebar': sidebar,
                'translation': obj
            }
            content = render_to_string(self.DOC_CONTENT_TEMPLATE, context)
            fp = FlatPage.objects.filter(url=obj.get_absolute_url())
            if fp.count():
                # dokumentace jiz v podobe FlatPage existuje
                # aktualizujeme ji...
                fp = fp[0]
                fp.title = title
                fp.content = content
                fp.save()
            else:
                # dokumentace v podobe FlatPage neexistuje
                # vytvorime ji...
                fp = FlatPage(
                    url = obj.get_absolute_url(),
                    title = title,
                    content = content,
                    enable_comments = False,
                    registration_required = False
                )
                fp.save()
                site = Site.objects.get_current()
                fp.sites.add(site)
            obj.flat_page = fp
            obj.save()

    def run_sphinx(self):
        """
        Vygeneruje HTML dokumentaci spustenim externi aplikace Sphinx v adresari
        s Django dokumentaci.
        """
        self._rewrite_original_docs()
        return doc_build()

class Translation(models.Model):
    """
    Model reprezentujici preklad konkretniho souboru v oficialni
    dokumentaci v Djangu.

    Model uklada informaci o tom JAKA dokumentace je preklada,
    v jake REVIZI, ktery UZIVATEL ma s prekladem co do cineni
    a odkaz na HTML podobu prelozene dokumentace.
    """
    source_path = models.FilePathField(u"Cesta k originálu", path=settings.DOC_PATH, match=r"\.txt$", recursive=True, unique=True, help_text=u"Cesta k originalni dokumentaci v anglictine, pro kterou je vytvoren zde editovany preklad. Obsah souboru je naformatovan v ReSTu (Sphinx).")
    revision = models.IntegerField(u"Revize překladu", help_text=u"Cislo revize originalniho dokumentace v anglictine, ze ktere se preklad udelal.")
    users = models.ManyToManyField(User, through="TranslationRole")
    content = models.TextField(u"Překlad", help_text=u"Preklad anglicke dokumentace z pole 'Cesta k originalu'. Obsah je naformatovan v ReSTu (Sphinx).")
    flat_page = models.ForeignKey(FlatPage, blank=True, null=True, help_text=u"Stranka, ktera obsahuje HTML podobu prekladu (generuje se automaticky z pole 'Preklad').", editable=False)
    created = models.DateTimeField(u"Datum vytvoření", editable=False)
    updated = models.DateTimeField(u"Datum aktualizace", editable=False)
    objects = TranslationManager()

    class Meta:
        verbose_name = u"Překlad"
        verbose_name_plural = u"Překlady"
        ordering = ("source_path", )

    def __unicode__(self):
        return "%s, revision %i" % (self.short_source_path, self.revision)

    def get_short_source_path(self):
        """Zkracena cesta k original dokumentaci (relativne k DOC_PATH)."""
        # TODO: testy
        return self.source_path[len(settings.DOC_PATH)+1:]
    get_short_source_path.short_description = u'Cesta k originálu'
    short_source_path = property(get_short_source_path)

    def get_source_html_path(self):
        """Absolutni cesta k vygenerovane HTML dokumentaci."""
        # TODO: testy
        return os.path.join(settings.DOC_PATH, '_build/html/' + self.html_id + '.html')
    source_html_path = property(get_source_html_path)

    def get_source_html_content(self):
        """Vrati obsah HTML dokumentace."""
        # TODO: testy
        f = open(self.source_html_path)
        content = f.read()
        f.close()
        return content.decode('utf-8')
    source_html_content = property(get_source_html_content)

    def get_html_id(self):
        """
        ID dokumentu, napr. pro dokument "intro/overview.html" 
        vrati fce "intro/overview".
        """
        # TODO: testy
        bits = self.source_path.split('/')
        return bits[-2] + '/' + bits[-1][:bits[-1].rfind('.')]
    html_id = property(get_html_id)

    def get_absolute_url(self):
        """
        Vrati URL na prelozeny dokument.
        """
        # TODO: testy
        return settings.DOC_URL + self.html_id + '/'

    def save(self, force_insert=False, force_update=False):
        now = datetime.now()
        if not self.id:
            self.created = now
        self.updated = now
        super(Translation, self).save(force_insert, force_update)

    def rewrite(self):
        """
        Prepise originalni soubor `self.source_path` v adresari DOC_PATH 
        obsahem `self.content`.
        """
        return doc_rewrite_if_not_same(self.source_path, self.content)

    def is_actual(self):
        """
        TODO:
        - v pripade neaktualnosti by se mohl generovat link na diff do django tracu
        """
        new_rev = doc_last_change_revision(self.source_path)
        return (self.revision >= new_rev, self.revision, new_rev)


class TranslationRole(models.Model):
    """
    Ke kazdemu prekladu muze byt prirazen uzivatel v konkretni roli
    (prekladatel, korektor, apod).
    """
    ROLE_CHOICE_TRANSLATION = 'preklad'
    ROLE_CHOICE_CORECTION = 'korekce'
    ROLE_CHOICES = (
        (ROLE_CHOICE_TRANSLATION, u'Překlad'),
        (ROLE_CHOICE_CORECTION, u'Korekce'),
    )

    translation = models.ForeignKey(Translation)
    user = models.ForeignKey(User)
    role = models.CharField(u"Role", max_length=128, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = u"Role překladatele"
        verbose_name_plural = u"Role překladatelů"
        ordering = ('user', )
