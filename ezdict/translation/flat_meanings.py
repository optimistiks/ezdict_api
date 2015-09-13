from translators import YA_DICT_URL, YA_DICT_KEY
import goslate
import requests


def getFlatMeanings(text, targetLang):
    gs = goslate.Goslate()
    sourceLang = gs.detect(text)
    translation = gs.translate(text, targetLang, sourceLang)

    dictDir = sourceLang + '-' + targetLang
    response = requests.get(
        (YA_DICT_URL + '&lang=%(dictDir)s&text=%(text)s') % {'yaDictKey': YA_DICT_KEY, 'dictDir': dictDir,
                                                             'text': text})
    yaDict = response.json()

    meanings = set()
    meanings.add(translation.lower())
    if len(yaDict['def']):
        for yaDef in yaDict['def']:
            for yaDefTr in yaDef['tr']:
                meaning = yaDefTr['text'].lower()
                meanings.add(meaning)
                if 'syn' in yaDefTr:
                    for yaDefTrSyn in yaDefTr['syn']:
                        meaning = yaDefTrSyn['text'].lower()
                        meanings.add(meaning)

    return meanings
