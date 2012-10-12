# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

import os
import re
from django.conf import settings
from django.utils.encoding import force_unicode



class DjczMiddleware(object):
    """
    TODO:
    """       
    KEYS = {
        u'<!-- INC:djangopeople -->': 'djangopeople.html',
        u'<!-- INC:djangosites -->': 'djangosites.html',
        u'<!-- INC:irc -->': 'irc.html',
    }
    IGNORED_FILES = re.compile(r'\.(css|jpg|png|gif)$')

    def process_response(self, request, response):
        if self.IGNORED_FILES.search(request.META['PATH_INFO']):
            return response
        if 'text/html' not in response['Content-Type']:
            return response
        
        content = force_unicode(response.content)
        for k in self.KEYS:
            if content.find(k) != -1:
                # try:
                #     f = open(os.path.join(FETCHER_CACHE_PATH, self.KEYS[k]))
                #     c = f.read()
                #     f.close()
                #     content = content.replace(k, force_unicode(c))
                # except:
                #     pass
                f = open(os.path.join(settings.FETCHER_CACHE_PATH, self.KEYS[k]))
                c = f.read()
                f.close()
                content = content.replace(k, force_unicode(c))

        response.content = content
        return response
