# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

"""
########################################
### Testy ukladani pro model Translation
########################################

>>> from djcz.translations.models import Translation

# Ulozime treti preklad
>>> t3 = Translation(revision=3, source_path='intro/tutorial02.txt', content='toto je uplne jiny obsah')
>>> t3.save()


# Vytahneme treti preklad z DB (instance uz ma nastaveno ID)
# ZAMERNE zmenime source_path na stejny soubor, jako ma t1
# Opet se vyvola vyjimka
>>> t = Translation.objects.get(revision=3)
>>> t.source_path = 'intro/tutorial01.txt'
>>> t.save()
Traceback (most recent call last):
    ...
IntegrityError: duplicate key violates unique constraint "translations_translation_source_path_key"
<BLANKLINE>
"""
