# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

"""
Pomocne funkce.
"""

import subprocess
import re
from django.conf import settings
from apps.tools.BeautifulSoup import BeautifulSoup, NavigableString

def doc_is_same(path, new_content):
    """
    Zkontroluje, jestli je obsah zadaneho souboru `path` stejny
    jako retezec `new_content`.
    """
    f = open(path, 'r')
    old_content = f.read()
    f.close()
    return old_content == new_content

def doc_rewrite(path, new_content):
    """
    Prepise zadany soubor obsahem `new_content`.
    """
    f = open(path, 'w')
    f.write(new_content.encode('utf-8'))
    f.close()

def doc_rewrite_if_not_same(path, new_content):
    """
    Prepise zadany soubor obsahem `new_content`, pokud
    je se jeho obsah lisi.

    Vraci True, pokud soubor prepise.
    """
    if not doc_is_same(path, new_content):
        doc_rewrite(path, new_content)
        return True
    return False

def doc_build():
    """
    "Zkompiluje" dokumentaci prostrednictvim Sphinx, tj. prevede
    ReST do HTML podoby a vsecko mezi sebou pekne prolinkuje.

    Vraci stdout a stderr (seznam retezcu)

    Typicky vystup z fce doc_build:

    Prvni spusteni
    --------------

    child_stdout:
        ['mkdir -p _build/html _build/doctrees\n',
         'sphinx-build -b html -d _build/doctrees   . _build/html\n',
         'Sphinx v0.4.2, building html\n',
         'trying to load pickled env... not found\n',
         'building [html]: targets for 133 source files that are out of date\n',
         'updating environment: 133 added, 0 changed, 0 removed\n',
         'reading... contents faq/admin faq/contributing faq/general faq/help faq/index faq/install faq/models faq/usage glossary howto/apache-auth howto/custom-file-storage howto/custom-management-commands howto/custom-model-fields howto/custom-template-tags howto/deployment/fastcgi howto/deployment/index howto/deployment/modpython howto/error-reporting howto/index howto/initial-data howto/jython howto/legacy-databases howto/outputting-csv howto/outputting-pdf howto/static-files index internals/committers internals/contributing internals/documentation internals/index internals/release-process intro/index intro/install intro/overview intro/tutorial01 intro/tutorial02 intro/tutorial03 intro/tutorial04 intro/whatsnext misc/api-stability misc/design-philosophies misc/distributions misc/index obsolete/admin-css obsolete/index ref/contrib/admin ref/contrib/auth ref/contrib/comments/index ref/contrib/comments/settings ref/contrib/comments/signals ref/contrib/comments/upgrade ref/contrib/contenttypes ref/contrib/csrf ref/contrib/databrowse ref/contrib/flatpages ref/contrib/formtools/form-preview ref/contrib/formtools/form-wizard ref/contrib/formtools/index ref/contrib/humanize ref/contrib/index ref/contrib/localflavor ref/contrib/redirects ref/contrib/sitemaps ref/contrib/sites ref/contrib/syndication ref/contrib/webdesign ref/databases ref/django-admin ref/files/file ref/files/index ref/files/storage ref/forms/api ref/forms/fields ref/forms/index ref/forms/validation ref/forms/widgets ref/generic-views ref/index ref/middleware ref/models/fields ref/models/index ref/models/instances ref/models/options ref/models/querysets ref/models/relations ref/request-response ref/settings ref/signals ref/templates/api ref/templates/builtins ref/templates/index ref/unicode releases/0.95 releases/0.96 releases/1.0 releases/1.0-alpha-1 releases/1.0-alpha-2 releases/1.0-beta releases/1.0-beta-2 releases/1.0-porting-guide releases/index topics/auth topics/cache topics/db/index topics/db/managers topics/db/models topics/db/queries topics/db/sql topics/db/transactions topics/email topics/files topics/forms/formsets topics/forms/index topics/forms/media topics/forms/modelforms topics/http/file-uploads topics/http/generic-views topics/http/index topics/http/middleware topics/http/sessions topics/http/shortcuts topics/http/urls topics/http/views topics/i18n topics/index topics/install topics/pagination topics/serialization topics/settings topics/signals topics/templates topics/testing \n',
         'pickling the env... done\n',
         'checking consistency...\n',
         'writing output... contents faq/admin faq/contributing faq/general faq/help faq/index faq/install faq/models faq/usage glossary howto/apache-auth howto/custom-file-storage howto/custom-management-commands howto/custom-model-fields howto/custom-template-tags howto/deployment/fastcgi howto/deployment/index howto/deployment/modpython howto/error-reporting howto/index howto/initial-data howto/jython howto/legacy-databases howto/outputting-csv howto/outputting-pdf howto/static-files index internals/committers internals/contributing internals/documentation internals/index internals/release-process intro/index intro/install intro/overview intro/tutorial01 intro/tutorial02 intro/tutorial03 intro/tutorial04 intro/whatsnext misc/api-stability misc/design-philosophies misc/distributions misc/index obsolete/admin-css obsolete/index ref/contrib/admin ref/contrib/auth ref/contrib/comments/index ref/contrib/comments/settings ref/contrib/comments/signals ref/contrib/comments/upgrade ref/contrib/contenttypes ref/contrib/csrf ref/contrib/databrowse ref/contrib/flatpages ref/contrib/formtools/form-preview ref/contrib/formtools/form-wizard ref/contrib/formtools/index ref/contrib/humanize ref/contrib/index ref/contrib/localflavor ref/contrib/redirects ref/contrib/sitemaps ref/contrib/sites ref/contrib/syndication ref/contrib/webdesign ref/databases ref/django-admin ref/files/file ref/files/index ref/files/storage ref/forms/api ref/forms/fields ref/forms/index ref/forms/validation ref/forms/widgets ref/generic-views ref/index ref/middleware ref/models/fields ref/models/index ref/models/instances ref/models/options ref/models/querysets ref/models/relations ref/request-response ref/settings ref/signals ref/templates/api ref/templates/builtins ref/templates/index ref/unicode releases/0.95 releases/0.96 releases/1.0 releases/1.0-alpha-1 releases/1.0-alpha-2 releases/1.0-beta releases/1.0-beta-2 releases/1.0-porting-guide releases/index topics/auth topics/cache topics/db/index topics/db/managers topics/db/models topics/db/queries topics/db/sql topics/db/transactions topics/email topics/files topics/forms/formsets topics/forms/index topics/forms/media topics/forms/modelforms topics/http/file-uploads topics/http/generic-views topics/http/index topics/http/middleware topics/http/sessions topics/http/shortcuts topics/http/urls topics/http/views topics/i18n topics/index topics/install topics/pagination topics/serialization topics/settings topics/signals topics/templates topics/testing \n',
         'finishing... \n',
         'writing additional files... genindex modindex search\n',
         'copying images... obsolete/_images/objecttools_01.gif intro/_images/admin08t.png intro/_images/admin12.png intro/_images/admin04t.png obsolete/_images/formrow.gif topics/http/_images/middleware.png intro/_images/admin10.png ref/contrib/_images/flatfiles_admin.png intro/_images/admin06t.png intro/_images/admin03t.png intro/_images/admin13t.png intro/_images/admin07.png intro/_images/admin05t.png obsolete/_images/module.gif ref/contrib/_images/users_changelist.png intro/_images/admin09.png obsolete/_images/objecttools_02.gif intro/_images/admin01.png intro/_images/admin11t.png intro/_images/admin02t.png intro/_images/admin14t.png internals/_images/djangotickets.png\n',
         'copying static files...\n',
         'dumping search index...\n',
         'build succeeded, 1 warning.\n',
         '\n',
         'Build finished. The HTML pages are in _build/html.\n']
    child_stderr:
        ["WARNING: /home/msgre/projects/www/djangoproject.cz/docs/index.txt:: document isn't included in any toctree\n"]


    Dalsi spusteni (zadna zmena v souborech)
    ----------------------------------------

    child_stdout:
        ['mkdir -p _build/html _build/doctrees\n',
         'sphinx-build -b html -d _build/doctrees   . _build/html\n',
         'Sphinx v0.4.2, building html\n',
         'trying to load pickled env... done\n',
         'building [html]: targets for 0 source files that are out of date\n',
         'updating environment: 0 added, 0 changed, 0 removed\n',
         'no targets are out of date.\n',
         '\n',
         'Build finished. The HTML pages are in _build/html.\n']
    child_stderr:
        []


    Dalsi spusteni (jedna zmena v souboru intro/overview.txt)
    ---------------------------------------------------------

    child_stdout:
        ['mkdir -p _build/html _build/doctrees\n',
         'sphinx-build -b html -d _build/doctrees   . _build/html\n',
         'Sphinx v0.4.2, building html\n',
         'trying to load pickled env... done\n',
         'building [html]: targets for 1 source files that are out of date\n',
         'updating environment: 0 added, 1 changed, 0 removed\n',
         'reading... intro/overview \n',
         'pickling the env... done\n',
         'checking consistency...\n',
         'writing output... contents intro/index intro/overview \n',
         'finishing... \n',
         'writing additional files... genindex modindex search\n',
         'copying static files...\n',
         'dumping search index...\n',
         'build succeeded, 1 warning.\n',
         '\n',
         'Build finished. The HTML pages are in _build/html.\n']

    child_stderr:
        ["WARNING: /home/msgre/projects/www/djangoproject.cz/docs/index.txt:: document isn't included in any toctree\n"]

    """
    cmd = 'cd %s; make html' % settings.DOC_PATH
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    return [i.strip() for i in p.stdout.readlines() if i.strip()], [i.strip() for i in p.stderr.readlines() if i.strip()], 

def doc_update(revision=None):
    """
    Zaktualizuje lokalni kopii Django dokumentace. Pokud je zadan
    parametr revision, updatne se lokalni verze na zadanou revizi,
    v opacnem pripade se zaktualizuje na nejnovejsi.

    Dela to mozna slozite, ale ciste: vsechny lokalni modifikace
    v pracovni kopii dokumentace se revertou, a teprve pote se 
    provede aktualizaci pres svn.

    Jeden z moznych vystupu fce:

        {'modified_files': ['intro/overview.txt\n'],
         'revert_stderr': [],
         'revert_stdout': ["Reverted 'intro/overview.txt'\n"],
         'update_stderr': [],
         'update_stdout': ['At revision 9462.\n']}
    """
    out = {'revert_stdout':[], 'revert_stderr':[]}
    # seznam lokalne modifikovanych souboru
    cmd = 'cd %s; svn st | grep ^M' % settings.DOC_PATH
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True)
    out['modified_files'] = [i[7:] for i in p.stdout]
    # svn revert pro lokalni modifikace
    if out['modified_files']:
        cmd2 = 'cd %s; svn revert %s' % (settings.DOC_PATH, " ".join(out['modified_files']))
        p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        out['revert_stdout'] = p2.stdout.readlines()
        out['revert_stderr'] = p2.stderr.readlines()
    # svn up
    cmd3 = 'cd %s; ' % settings.DOC_PATH
    if revision:
        cmd3 += 'svn -r%i up' % revision
    else:
        cmd3 += 'svn up'
    p3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out['update_stdout'] = p3.stdout.readlines()
    out['update_stderr'] = p3.stderr.readlines()
    return out

def doc_last_change_revision(path):
    """
    TODO:
    """
    TERM = 'Last Changed Rev:'
    cmd = 'svn info %s | grep "^%s"' % (path, TERM)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True)
    rev = p.stdout.readlines()[0][len(TERM):]
    return int(rev.strip())

class DocHtmlProcessor(object):
    """
    Trida, ktera zpracuje vygenerovanou HTML dokumentaci.
    TODO: testy
    """
    def __init__(self, html, content_id):
        self.html = html
        self.content_id = content_id # id <div> s obsahem
        self.directory = content_id[:content_id.find('-')] # prvni cast id (do znaku '-')
        self.RE_URL = re.compile(r'href="([^"#]+)(#[^"]+)?"')
        # regularni vyrazy pro prepis href odkazu
        self.RE_HREFS = (
            (re.compile(r'href="([^\."]+)\.html"'), r'href="%s/\1/"' % (settings.DOC_URL + self.directory),), # href="tutorial03.html
            (re.compile(r'href="([^\."]+)\.html(#[^"]+)"'), r'href="%s/\1/\2"' % (settings.DOC_URL + self.directory),), # href="tutorial03.html#intro-tutorial03"
            (re.compile(r'href="(\.\.)\/([^/"]+)\/([^\.]+).html"'), r'href="%s\2/\3/"' % settings.DOC_URL), # href="../ref/settings.html
            (re.compile(r'href="(\.\.)\/([^/"]+)\/([^\.]+).html(#[^"]+)"'), r'href="%s\2/\3/\4"' % settings.DOC_URL), # href="../ref/settings.html#setting-INSTALLED_APPS"
            (re.compile(r'href="(\.\.)\/([^\.]+).html"'), r'href="%s\2/"' % settings.DOC_URL), # href="../index.html"
            (re.compile(r'href="(\.\.)\/([^\.]+).html(#[^"]+)"'), r'href="%s\2/\3"' % settings.DOC_URL), # href="../index.html#neco"
        )
        # regularni vyrazy pro prepis src odkazu (na obrazky)
        self.RE_SRCS = (
            (re.compile(r'src="\.\.\/_images\/([^"]+)"'), r'src="%simages/\1"' % settings.MEDIA_URL), # <img alt="Hlavní správcovská stránka" src="../_images/admin02t.png" />
        )
        # regularni vyrazy pro prepis fragmentu anglickych textu
        self.RE_ENGLISH_FRAGMENTS = (
            (re.compile(r'<h3>Table Of Contents</h3>'), ur'<h3>Obsah</h3>'),
            (re.compile(r'<h3>Browse</h3>'), ur'<h3>Listování</h3>'),
            (re.compile(r'<li>Prev(: <a[^>]+>[^<]+</a>)</li>'), ur'<li>Předchozí\1</li>'),
            (re.compile(r'<li>Next(: <a[^>]+>[^<]+</a>)</li>'), ur'<li>Další\1</li>'),
            (re.compile(r'(<a.+?title=")Permalink to this headline("[^>]*>)'), ur'\1Permalink na tento nadpis\2'),
            (re.compile(r'(<p class="first admonition-title">)Warning(</p>)'), ur'\1Upozornění\2'),
            (re.compile(r'(<p class="first admonition-title">)Note(</p>)'), ur'\1Poznámka\2'),
        )

    def translate(self):
        """Preklad anglickych fragmentu ve strance."""
        for item in self.RE_ENGLISH_FRAGMENTS:
            self.html = item[0].sub(item[1], self.html)

    def hrefs(self, translated_urls):
        """
        Uprava odkazu: strankam, ktere mame prelozene (viz `translated_urls`),
        upravime URL tak, aby vedly do nasi aplikace. Ostatnim pridame
        prefix v podobe absolutni URL na oficialni dokumentaci.
        """
        for item in self.RE_HREFS:
            for i in item[0].finditer(self.html):
                replacement = i.expand(item[1])
                url = self.RE_URL.search(replacement)
                if not url:
                    continue
                if url.group(1) not in translated_urls: 
                    replacement = replacement.replace(settings.DOC_URL, settings.OFFICIAL_DOC_URL)
                self.html = self.html.replace(i.group(0), replacement)

    def srcs(self):
        """Uprava odkazu na obrazky."""
        for item in self.RE_SRCS:
            for i in item[0].finditer(self.html):
                replacement = i.expand(item[1])
                self.html = self.html.replace(i.group(0), replacement)

    def _split_title(self):
        """Vytahne titulek stranky."""
        title = self.soup.find('title').string
        if title.find('&mdash') != -1:
            title = title[:title.find('&mdash')].strip()
        return title

    def _split_content(self, content_id):
        """Vytahne obsah stranky."""
        content = self.soup.find(id=content_id).find('div')
        return unicode(content)

    def _split_sidebar(self):
        """Vytahne sidebar ze stranky."""
        _sidebar = self.soup.find(id='sidebar').find('div').find('div').contents
        count = 0
        sidebar = []
        for item in _sidebar:
            if type(item) == NavigableString: continue
            if item.name == u'h3':
                if count > 1: break
                count += 1
            sidebar.append(u"%s" % item)
        return u"".join(sidebar)

    def split(self):
        """Vrati casti z HTML dokumentu, ktere nas zajimaji."""
        title = self._split_title()
        content = self._split_content(self.content_id)
        sidebar = self._split_sidebar()
        return title, content, sidebar

    def process(self, translated_urls=[]):
        """Kompletni zpracovani HTML dokumentace."""
        self.translate()
        self.hrefs(translated_urls)
        self.srcs()
        self.soup = BeautifulSoup(self.html)
        return self.split()
