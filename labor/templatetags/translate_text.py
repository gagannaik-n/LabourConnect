
from django import template
from django.utils.translation import get_language
from config.translations import TRANSLATIONS

register = template.Library()


@register.simple_tag(takes_context=True)
def tr(context, text):
    language = get_language() or "en"

    translations = TRANSLATIONS.get(
        language.split("-")[0],
        TRANSLATIONS["en"]
    )

    return translations.get(text, text)
