import goslate
import requests
import operator
from ezdict.card.models import Card
from ezdict.card.serializers import CardSerializer
from ezdict.translation_history.models import TranslationHistory
from ezdict.translation_history.serializers import TranslationHistorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.utils.translation import ugettext as _

YA_DICT_KEY = 'dict.1.1.20131027T115553Z.881398786442095e.51bb0420197e3eecd21c1dff059a2636b3976867'


class TranslationView(APIView):
    """
    View to translate strings
    """

    def getText(self, request):
        text = request.query_params.get('string', None)
        if text is None:
            raise serializers.ValidationError(_('Parameter %(param)s is required.') % {'param': 'string'})
        text = text.strip().lower()
        return text

    def getLang(self, request):
        lang = request.query_params.get('lang', None)
        if lang is None:
            raise serializers.ValidationError(_('Parameter %(param)s is required.') % {'param': 'lang'})
        lang = lang.strip().lower()
        return lang

    def initHistorySerializer(self, request, string):
        history = TranslationHistory().findByUserAndString(request.user, string)
        if history is not None:
            historySerializer = TranslationHistorySerializer(history, data={'string': history.string},
                                                             context={'request': request})
        else:
            historySerializer = TranslationHistorySerializer(data={'string': string}, context={'request': request})
        return historySerializer

    def initCardSerializer(self, request, text):
        cardSerializer = None
        card = Card().findByUserAndText(request.user, text)
        if card is not None:
            cardSerializer = CardSerializer(card, context={'request': request})
        return cardSerializer

    def get(self, request):
        """
        ---
        parameters:
            - name: string
              description: a string to translate
              required: true
              type: string
              paramType: query
            - name: lang
              description: a target language
              required: true
              type: string
              paramType: query
        """
        text = self.getText(request)
        targetLang = self.getLang(request)

        historySerializer = self.initHistorySerializer(request, text)
        historySerializer.is_valid(raise_exception=True)
        historySerializer.save(user=request.user)

        gs = goslate.Goslate()
        sourceLang = gs.detect(text)
        translation = gs.translate(text, targetLang, sourceLang)

        dictDir = sourceLang + '-' + targetLang
        dictUrl = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=%(yaDictKey)s'
        dict = requests.get(
            (dictUrl + '&lang=%(dictDir)s&text=%(text)s') % {'yaDictKey': YA_DICT_KEY, 'dictDir': dictDir,
                                                             'text': text})

        response = {
            'translation_history': historySerializer.data,
            'translation': translation,
            'ya_dict': dict.json()
        }

        cardSerializer = self.initCardSerializer(request, text)

        if cardSerializer is not None:
            response['card'] = cardSerializer.data

        return Response(response, status=status.HTTP_200_OK)


class LanguageView(APIView):
    """
    View to get available languages
    """

    def get(self, request):
        keys = ['code', 'name']
        languages = goslate.Goslate().get_languages()
        sortedLanguages = sorted(languages.items(), key=operator.itemgetter(1))
        listOfDicts = [dict(zip(keys, row)) for row in sortedLanguages]
        return Response(listOfDicts, status=status.HTTP_200_OK)
