# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

import re
from django import forms
from models import Translation

DOC_FILES_RE = re.compile(r'^/[^_].+$') # vse co za lomitkem zacina na _ ignoruj

class TranslationAdminForm(forms.ModelForm):
    """
    Custom formular pro admin. Jeho role je jedina -- zuzit seznam choices
    pro pole source_path (v ceste se mohou vyskytovat i soubory z adresare
    _build, ktery vznikne po kompilaci dokumentace sphinxem) a setridit jej.
    """
    class Meta:
        model = Translation

    def __init__(self, *args, **kwargs):
        super(TranslationAdminForm, self).__init__(*args, **kwargs)
        choices = [i for i in self.fields['source_path'].choices if DOC_FILES_RE.match(i[1])]
        self.fields['source_path'].choices = sorted(choices, cmp=lambda x,y: cmp(x[1], y[1]))
