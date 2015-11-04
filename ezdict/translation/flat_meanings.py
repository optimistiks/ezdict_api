from django.conf import settings
import requests
from translator import translator


def get_flat_meanings(text, target_lang):
    source_lang = translator.detect_language(text)
    translation = translator.translate(text, target_lang, source_lang)

    dict_dir = source_lang + '-' + target_lang
    response = requests.get(
        (settings.YA_TRANSLATOR['URL'] + '&lang=%(dictDir)s&text=%(text)s') % {
            'yaDictKey': settings.YA_TRANSLATOR['KEY'],
            'dictDir': dict_dir,
            'text': text
        })
    ya_dict = response.json()

    meanings = set()
    meanings.add(translation.lower())
    if len(ya_dict['def']):
        for yaDef in ya_dict['def']:
            for yaDefTr in yaDef['tr']:
                meaning = yaDefTr['text'].lower()
                meanings.add(meaning)
                if 'syn' in yaDefTr:
                    for yaDefTrSyn in yaDefTr['syn']:
                        meaning = yaDefTrSyn['text'].lower()
                        meanings.add(meaning)

    return meanings
