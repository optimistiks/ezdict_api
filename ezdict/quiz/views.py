from models import Quiz
from serializers import QuizSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import (
    BulkModelViewSet,
)
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class QuizViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    A ViewSet for working with quizzes.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    ordering = ('-created',)
