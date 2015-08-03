import goslate
import requests
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

    def getString(self, request):
        string = request.query_params.get('string', None)
        if string is None:
            raise serializers.ValidationError(_('Parameter %(param)s is required.') % {'param': 'string'})
        string = string.strip().lower()
        return string

    def initHistorySerializer(self, request, string):
        history = TranslationHistory().findByUserAndString(request.user, string)
        if history is not None:
            historySerializer = TranslationHistorySerializer(history, data={'string': history.string},
                                                             context={'request': request})
        else:
            historySerializer = TranslationHistorySerializer(data={'string': string}, context={'request': request})
        return historySerializer

    def get(self, request):
        """
        ---
        parameters:
            - name: string
              description: a string to translate
              required: true
              type: string
              paramType: query
        """
        string = self.getString(request)

        historySerializer = self.initHistorySerializer(request, string)
        historySerializer.is_valid(raise_exception=True)
        historySerializer.save(user=request.user)

        gs = goslate.Goslate()
        sourceLang = gs.detect(string)
        translation = gs.translate(string, 'ru')

        dictDir = sourceLang + '-ru'
        dictUrl = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=%(yaDictKey)s'
        dict = requests.get(
            (dictUrl + '&lang=%(dictDir)s&text=%(text)s') % {'yaDictKey': YA_DICT_KEY, 'dictDir': dictDir,
                                                             'text': string})

        response = {
            'translation_history': historySerializer.data,
            'translation': translation,
            'ya_dict': dict.json()
        }

        return Response(response, status=status.HTTP_200_OK)
