from models import Card
from serializers import CardSerializer
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
