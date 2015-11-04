import requests
import json

from ezdict.card.models import Card
from ezdict.card.serializers import CardSerializer

from ezdict.translation_history.models import TranslationHistory
from ezdict.translation_history.serializers import TranslationHistorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from django.utils.translation import ugettext as _, get_language
from django.conf import settings

from flat_meanings import get_flat_meanings
from translator import translator


class BaseTranslationView(APIView):
    """
    View to translate strings
    """

    @staticmethod
    def get_text(request):
        text = request.query_params.get('string', None)
        if text is None:
            raise serializers.ValidationError(_('Parameter %(param)s is required.') % {'param': 'string'})
        text = text.strip().lower()
        return text

    @staticmethod
    def get_lang(request):
        lang = request.query_params.get('lang', None)
        if lang is None:
            raise serializers.ValidationError(_('Parameter %(param)s is required.') % {'param': 'lang'})
        lang = lang.strip().lower()
        return lang

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
        pass


class TranslationView(BaseTranslationView):
    """
    View to translate strings
    """

    @staticmethod
    def init_history_serializer(request, string):
        history = TranslationHistory().findByUserAndString(request.user, string)
        if history is not None:
            history_serializer = TranslationHistorySerializer(history, data={'string': history.string},
                                                              context={'request': request})
        else:
            history_serializer = TranslationHistorySerializer(data={'string': string}, context={'request': request})
        return history_serializer

    @staticmethod
    def init_card_serializer(request, text):
        card_serializer = None
        card = Card().findByUserAndText(request.user, text)
        if card is not None:
            card_serializer = CardSerializer(card, context={'request': request})
        return card_serializer

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
        text = self.get_text(request)
        target_lang = self.get_lang(request)

        history_serializer = self.init_history_serializer(request, text)
        history_serializer.is_valid(raise_exception=True)
        history_serializer.save(user=request.user)

        source_lang = translator.detect_language(text)
        translation = ''

        ya_translation_direction = source_lang + '-' + target_lang
        ya_url = (settings.YA_TRANSLATOR['URL'] + '&lang=%(dictDir)s&text=%(text)s') % \
                 {
                     'yaDictKey': settings.YA_TRANSLATOR['KEY'],
                     'dictDir': ya_translation_direction,
                     'text': text
                 }

        ya_response = requests.get(ya_url)

        if ya_response.status_code != status.HTTP_200_OK or len(ya_response.json()['def']) == 0:
            translation = translator.translate(text, target_lang, source_lang)

        response = {
            'translation_history': history_serializer.data,
            'translation': translation,
            'ya_dict': ya_response.json()
        }

        if ya_response.status_code == status.HTTP_200_OK:
            response['ya_dict'] = ya_response.json()
        else:
            response['ya_dict'] = {}

        card_serializer = self.init_card_serializer(request, text)

        if card_serializer is not None:
            response['card'] = card_serializer.data

        return Response(response, status=status.HTTP_200_OK)


class SuggestedMeaningView(BaseTranslationView):
    """
    View to get flat representation of text meanings
    """

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

        text = self.get_text(request)
        target_lang = self.get_lang(request)

        meanings = get_flat_meanings(text, target_lang)

        return Response(meanings, status=status.HTTP_200_OK)


class LanguageView(APIView):
    """
    View to get available languages
    """

    def get(self, request):
        language_codes = translator.get_languages()
        language_names = translator.call('GetLanguageNames', {
            'locale': get_language(),
            'languageCodes': json.dumps(language_codes)
        })
        list_of_dicts = [{'code': code, 'name': name} for code, name in zip(language_codes, language_names)]
        list_of_dicts.sort(key=lambda lng: lng['name'])
        return Response(list_of_dicts, status=status.HTTP_200_OK)
