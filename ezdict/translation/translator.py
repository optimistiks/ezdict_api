from microsofttranslator import Translator
from django.conf import settings


translator = Translator(settings.BING_TRANSLATOR['CLIENT_ID'], settings.BING_TRANSLATOR['CLIENT_SECRET'])
