# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

"""
########################################
### Testy ukladani pro model Translation
########################################

>>> from djcz.translations.models import Translation

# Ulozime prvni preklad
>>> t1 = Translation(revision=1, source_path='intro/tutorial01.txt', content='toto je obsah')
>>> t1.save()


# Ulozime druhy preklad a SCHVALNE nastavime stejny zdrojovy soubor
# Nechceme, aby pro jeden soubor exitovalo vice prekladu, proto se vyvola vyjimka
>>> t2 = Translation(revision=2, source_path='intro/tutorial01.txt', content='toto je jiny obsah')
>>> t2.save()
Traceback (most recent call last):
    ...
IntegrityError: duplicate key violates unique constraint "translations_translation_source_path_key"
<BLANKLINE>
"""
