from django import http
from django.conf import settings

class SpammersMiddleware(object):
    def process_request(self, request):
        ip = request.META.get("REMOTE_ADDR", None)
        if ip and ip in settings.SPAMMER_IP:
            return http.HttpResponseForbidden('forbidden')
