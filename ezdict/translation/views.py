import goslate
from ezdict.translation_history.models import TranslationHistory
from ezdict.translation_history.serializers import TranslationHistorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers


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
            raise serializers.ValidationError('Parameter "string" is required')
        string = string.strip().lower()
        history = TranslationHistory().findByUserAndString(request.user, string)
        if history is not None:
            serializer = TranslationHistorySerializer(history, data={'string': history.string}, context={'request': request})
        else:
            serializer = TranslationHistorySerializer(data={'string': string}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(gs.translate(string, 'ru'))
