from models import TranslationHistory
from serializers import TranslationHistorySerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404


def getHistory(user, string):
    try:
        history = TranslationHistory.objects.get(user__exact=user.id,
                                                      string__iexact=string)
    except TranslationHistory.DoesNotExist:
        history = None
    return history


class TranslationCreateRetrieveView(APIView):
    """
    View to get and create translation history for string
    """

    def get(self, request):
        """
        ---
        parameters:
            - name: string
              description: a string to search translate history for
              required: true
              type: string
              paramType: query
        """
        string = request.query_params.get('string', None)
        if string is None:
            raise serializers.ValidationError('Parameter "string" is required')
        history = getHistory(self.request.user, string)
        if history is not None:
            serializer = TranslationHistorySerializer(history, context={'request': request})
            return Response(serializer.data)
        else:
            raise Http404('History not found')

    def post(self, request):
        """
        ---
        parameters:
            - name: string
              description: a string to create translate history for
              required: true
              type: string
              paramType: form
        """
        string = request.data.get('string', None)
        history = getHistory(self.request.user, string)
        if history is not None:
            serializer = TranslationHistorySerializer(history, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(count=history.count+1)
            return Response(serializer.data)
        else:
            serializer = TranslationHistorySerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
