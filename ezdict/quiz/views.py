from models import Quiz, QuizCard
from ezdict.card.models import Card
from serializers import QuizSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import (
    BulkModelViewSet,
)
from rest_framework import mixins, serializers
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import ugettext as _
from django.db import transaction
from django.db.models import Q


class QuizViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    A ViewSet for working with quizzes.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    ordering = ('-created',)

    @transaction.atomic
    def perform_create(self, serializer):
        cards = Card.objects.filter(
            Q(quiz_cards__isnull=True) | Q(quiz_cards__quiz__completed__isnull=False),
            to_study__isnull=False,
            user_id__exact=self.request.user.id
        )
        if cards:
            serializer.save()
            for card in cards:
                quizCard = QuizCard()
                quizCard.user = self.request.user
                quizCard.card = card
                quizCard.quiz = serializer.instance
                quizCard.save()
        else:
            raise serializers.ValidationError(_('There are no valid cards for quiz.'))

