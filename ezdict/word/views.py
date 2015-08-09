from models import WordToLearn, WordIsLearned
from serializers import WordToLearnSerializer, WordIsLearnedSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters


class WordToLearnViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    A ViewSet for working with words to learn.
    string -- a string to search words
    """
    queryset = WordToLearn.objects.all()
    serializer_class = WordToLearnSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('string',)
    ordering = ('-created',)


class WordIsLearnedViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A ViewSet for working with learned words.
    string -- a string to search words
    """
    queryset = WordIsLearned.objects.all()
    serializer_class = WordIsLearnedSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('string',)
    ordering = ('-created',)

