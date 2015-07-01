import goslate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers


class TranslationView(APIView):
    """
    View to translate strings
    string -- A string to translate
    """

    def get(self, request):
        gs = goslate.Goslate()
        string = request.query_params.get('string', None)
        if string is None:
            raise serializers.ValidationError('Parameter "string" is required')
        return Response(gs.translate(string, 'ru'))
