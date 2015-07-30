import goslate
from ezdict.translation_history.models import TranslationHistory
from ezdict.translation.serializers import TranslationSerializer
from ezdict.translation_history.serializers import TranslationHistorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.utils.translation import ugettext as _


class TranslationView(APIView):
    """
    View to translate strings
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
        """
        gs = goslate.Goslate()
        string = request.query_params.get('string', None)
        if string is None:
            raise serializers.ValidationError(_('Parameter %(param)s is required.') % {'param': 'string'})
        string = string.strip().lower()
        history = TranslationHistory().findByUserAndString(request.user, string)
        if history is not None:
            historySerializer = TranslationHistorySerializer(history, data={'string': history.string},
                                                             context={'request': request})
        else:
            historySerializer = TranslationHistorySerializer(data={'string': string}, context={'request': request})
        historySerializer.is_valid(raise_exception=True)
        historySerializer.save(user=request.user)
        translation = gs.translate(string, 'ru')
        serializer = TranslationSerializer(
            data={
                'translation_history': historySerializer.data,
                'translation': translation
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
