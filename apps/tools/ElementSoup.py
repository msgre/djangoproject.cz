# $Id$
# element loader based on BeautifulSoup

# http://www.crummy.com/software/BeautifulSoup/
import BeautifulSoup as BS

# slightly silly
try:
    import xml.etree.cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        import elementtree.ElementTree as ET

import htmlentitydefs, re

pattern = re.compile("&(\w+);")

def unescape(string):
    # work around oddities in BeautifulSoup's entity handling
    def unescape_entity(m, defs=htmlentitydefs.name2codepoint):
        try:
            return unichr(defs[m.group(1)])
        except KeyError:
            return m.group(0) # use as is
    return pattern.sub(unescape_entity, string)

##
# Loads an XHTML or HTML file into an Element structure, using Leonard
# Richardson's tolerant BeautifulSoup parser.
#
# @param file Source file (either a file object or a file name).
# @param builder Optional tree builder.  If omitted, defaults to the
#     "best" available <b>TreeBuilder</b> implementation.
# @return An Element instance representing the HTML root element.

def parse(file, builder=None, encoding=None):
    bob = builder
    def emit(soup):
        if isinstance(soup, BS.NavigableString):
	    if isinstance(soup, BS.Comment):
		return
            bob.data(unescape(soup))
        else:
            bob.start(soup.name, dict((k, unescape(v)) for k, v in soup.attrs))
            for s in soup:
                emit(s)
            bob.end(soup.name)
    # determine encoding (the document charset is not reliable)
    if not hasattr(file, "read"):
        file = open(file)
    text = file.read()
    if not encoding:
        try:
            encoding = "utf-8"
            unicode(text, encoding)
        except UnicodeError:
            encoding = "iso-8859-1"
    soup = BS.BeautifulSoup(
        text, convertEntities="html", fromEncoding=encoding
        )
    # build the tree
    if not bob:
        bob = ET.TreeBuilder()
    emit(soup)
    root = bob.close()
    # wrap the document in a html root element, if necessary
    if len(root) == 1 and root[0].tag == "html":
        return root[0]
    root.tag = "html"
    return root

if __name__ == "__main__":
    import sys
    source = sys.argv[1]
    if source.startswith("http:"):
	import urllib
	source = urllib.urlopen(source)
    print ET.tostring(parse(source))
