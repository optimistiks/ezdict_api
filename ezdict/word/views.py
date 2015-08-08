from models import WordToLearn, WordIsLearned
from serializers import WordToLearnSerializer, WordIsLearnedSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


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
    filter_fields = ('string',)


class WordIsLearnedViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A ViewSet for working with learned words.
    string -- a string to search words
    """
    queryset = WordIsLearned.objects.all()
    serializer_class = WordIsLearnedSerializer
    filter_fields = ('string',)
