# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

# NOTE:
# Pro spravnou funkci tohoto testu je nutne:
# * mit v systemu nainstalovane Subversion (svn) a Sphinx 
#   (http://sphinx.pocoo.org/)
# * mit v adresari DOC_PATH checkoutnutou oficialni dokumentaci Djanga
#   (http://code.djangoproject.com/svn/django/trunk/docs)
# * uzivatel, pod kterym se test spousti musi mit pravo zapisu
#   do adresare DOC_PATH

"""
##################################
### Testy kodu ze souboru utils.py
##################################

### Test diffu ###################

>>> import djcz.translations.utils
>>> from os.path import abspath, join, dirname, exists

# cesta k testovacimu souboru
>>> PATH = abspath(join(dirname(djcz.translations.utils.__file__), 'tests/index.txt'))

# new_content simuluje data z modelu Translation
>>> f = open(PATH)
>>> new_content = f.read()
>>> f.close()

# srovnani souboru a data
>>> djcz.translations.utils.doc_is_same(PATH, new_content)
True

>>> new_content += 'x'
>>> djcz.translations.utils.doc_is_same(PATH, new_content)
False


### Test prepsani souboru ########

# zapis si proverime na docasnem souboru
>>> PATH = PATH + '.bak'

# novy obsah
>>> rewrite_content = 'jedna veta staci'
>>> djcz.translations.utils.doc_rewrite(PATH, rewrite_content)
>>> djcz.translations.utils.doc_is_same(PATH, rewrite_content)
True

# prepsani souboru s kontrolou
>>> djcz.translations.utils.doc_is_same(PATH, new_content)
False
>>> djcz.translations.utils.doc_rewrite_if_not_same(PATH, new_content)
True
>>> djcz.translations.utils.doc_is_same(PATH, new_content)
True

# uklidime po sobe (pryc s docasnym souborem)
>>> from os import remove
>>> remove(PATH)


### Test generovani dokumentace ##

# nejdriv si uklidime v dokumentaci
# (mohlo se stat, ze predchozi test neprosel a zustal tam po nas binec)
>>> from django.conf import settings
>>> if exists(join(settings.DOC_PATH, 'intro/radegast.txt')): remove(join(settings.DOC_PATH, 'intro/radegast.txt'))
>>> if exists(join(settings.DOC_PATH, '_build/html/intro/radegast.html')): remove(join(settings.DOC_PATH, '_build/html/intro/radegast.html'))

# vygeneruje dokumentaci a overime si existenci souboru
>>> stdout, stderr = djcz.translations.utils.doc_build()
>>> exists(join(settings.DOC_PATH, 'intro/overview.txt'))
True
>>> exists(join(settings.DOC_PATH, '_build/html/intro/overview.html'))
True

# vytvorime fake soubor
>>> f = open(join(settings.DOC_PATH, 'intro/radegast.txt'), 'w')
>>> f.write('.. _intro-radegast:\\n')
>>> f.write('\\n')
>>> f.write('========\\n')
>>> f.write('Radegast\\n')
>>> f.write('========\\n')
>>> f.close()

# overime, zda se fake soubor vygeneroval do HTML podoby
>>> exists(join(settings.DOC_PATH, 'intro/radegast.txt'))
True
>>> exists(join(settings.DOC_PATH, '_build/html/intro/radegast.html'))
False
>>> stdout, stderr = djcz.translations.utils.doc_build()
>>> len([i for i in stdout if i in ('reading... intro/radegast \\n', 'writing output... contents intro/radegast \\n', )])
2
>>> len([i for i in stderr if i.find("radegast.txt:: document isn't included in any toctree") != -1])
1
>>> exists(join(settings.DOC_PATH, '_build/html/intro/radegast.html'))
True

# smazem fake soubor, i jeho HTML formu
>>> remove(join(settings.DOC_PATH, 'intro/radegast.txt'))
>>> remove(join(settings.DOC_PATH, '_build/html/intro/radegast.html'))
>>> stdout, stderr = djcz.translations.utils.doc_build() # uklidime po sobe


### Test aktualizace dokumentace #

>>> ret = djcz.translations.utils.doc_update(9452)
>>> ret = djcz.translations.utils.doc_update(9462)
>>> ret['modified_files']
[]
>>> ret['revert_stderr']
[]
>>> ret['revert_stdout']
[]
>>> ret['update_stderr']
[]
>>> ret['update_stdout']
['U    topics/auth.txt\\n', 'U    topics/forms/modelforms.txt\\n', 'U    topics/testing.txt\\n', 'U    topics/i18n.txt\\n', 'U    releases/1.0.1.txt\\n', 'U    faq/admin.txt\\n', 'U    ref/contrib/syndication.txt\\n', 'U    ref/models/querysets.txt\\n', 'U    ref/models/fields.txt\\n', 'U    ref/django-admin.txt\\n', 'U    ref/forms/fields.txt\\n', 'U    ref/settings.txt\\n', 'Updated to revision 9462.\\n']

# nakonec zaktualizujeme dokumentaci na posledni verzi
# (snad to nicemu vadit nebude)
>>> ret = djcz.translations.utils.doc_update()
"""
