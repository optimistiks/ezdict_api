from models import Card, CardMeaning
from serializers import CardSerializer, CardMeaningSerializer
from rest_framework.viewsets import ModelViewSet


class CardViewSet(ModelViewSet):
    """
    A ViewSet for working with cards.
    text -- a text to search card for
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_fields = ('text',)
    ordering = ('-created',)


class CardMeaningViewSet(ModelViewSet):
    """
    A ViewSet for working with card meanings.
    card -- a card to search meanings for
    """
    queryset = CardMeaning.objects.all()
    serializer_class = CardMeaningSerializer
    filter_fields = ('card',)
    ordering = ('-created',)
