# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

from models import Translation
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required


def regenerate(request):
    """
    Vygeneruje dokumentaci (zavola Sphinx), jeho HTML vystup zpracuje
    a vytvori z nej FlatPage objekty.
    """
    sphinx = Translation.objects.run_sphinx()
    Translation.objects.html_to_flatpage()
    return render_to_response(
        "admin/translations/translation/regenerate.html", {
            'sphinx_stdout': sphinx[0],
            'sphinx_stderr': sphinx[1],
            'app_label': Translation._meta.app_label,
            'verbose_name': Translation._meta.verbose_name_plural,
            'title': u'Přegenerování dokumentace'
        },
        RequestContext(request),
    )
regenerate = staff_member_required(regenerate)

