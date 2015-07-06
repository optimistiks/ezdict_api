from models import TranslationHistory
from serializers import TranslationHistorySerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class TranslationHistoryViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    string -- a string to search translate history for
    """
    queryset = TranslationHistory.objects.all()
    serializer_class = TranslationHistorySerializer
    filter_fields = ('string',)
