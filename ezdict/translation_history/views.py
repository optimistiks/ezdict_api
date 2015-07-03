from models import TranslationHistory
from serializers import TranslationHistorySerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


def getHistory(user, string):
    try:
        history = TranslationHistory.objects.get(user__exact=user.id,
                                                      string__iexact=string)
    except TranslationHistory.DoesNotExist:
        history = None
    return history


class TranslationHistoryViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    string -- a string to search translate history for
    """
    queryset = TranslationHistory.objects.all()
    serializer_class = TranslationHistorySerializer
    filter_fields = ('string',)
