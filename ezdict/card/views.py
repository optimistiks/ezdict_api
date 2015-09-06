from models import Card, CardMeaning
from serializers import CardSerializer, CardMeaningSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import (
    BulkModelViewSet,
)
from django_filters import FilterSet
from ezdict.ezdict_api.filters import ListFilter

class CardViewSet(ModelViewSet):
    """
    A ViewSet for working with cards.
    text -- a text to search card for
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_fields = ('text',)
    ordering = ('-created',)


class CardMeaningFilterSet(FilterSet):
    id = ListFilter(name='id')

    class Meta:
        model = CardMeaning
        fields = ['id', 'card']


class CardMeaningViewSet(BulkModelViewSet):
    """
    A ViewSet for working with card meanings.
    card -- a card to search meanings for
    """
    queryset = CardMeaning.objects.all()
    serializer_class = CardMeaningSerializer
    filter_class = CardMeaningFilterSet
    ordering = ('-created',)

    def allow_bulk_destroy(self, qs, filtered):
        modelId = self.request.query_params.get('id', None)
        return modelId is not None
