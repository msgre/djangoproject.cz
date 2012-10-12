# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

from django import template
from djcz.translations.models import TranslationRole

register = template.Library()

@register.inclusion_tag("translations/check_corector.html")
def check_corector(translation):
    """
    Zkontroluje pritomnost korektora u prekladu. Pokud zadneho
    nenajde, zobrazi na strance informativni hlasku s varovanim.
    """
    role = TranslationRole.ROLE_CHOICE_CORECTION
    return {
        'corected': translation.users.filter(translationrole__role=role).count()
    }

@register.inclusion_tag("translations/translation_info.html")
def translation_info(translation):
    """
    Vytiskne informace o prekladu (kdo stranku prelozil, jak je stara, apod.)
    """
    translator = TranslationRole.ROLE_CHOICE_TRANSLATION
    corector = TranslationRole.ROLE_CHOICE_CORECTION
    return {
        'translators': translation.users.filter(translationrole__role=translator),
        'corectors': translation.users.filter(translationrole__role=corector),
        'translation': translation
    }
