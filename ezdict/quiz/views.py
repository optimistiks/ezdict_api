from models import Quiz, QuizCard, QuizAnswer
from ezdict.card.models import Card, CardToStudy, CardIsLearned
from serializers import QuizSerializer, QuizAnswerSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import (
    BulkModelViewSet,
)
from rest_framework import mixins, serializers
from rest_framework_bulk import mixins as bulk_mixins
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import ugettext as _
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
import datetime


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

    @transaction.atomic
    def perform_create(self, serializer):
        now = timezone.now()
        twoWeeks = datetime.timedelta(weeks=2)
        cards = Card.objects.filter(to_study__isnull=False, user_id__exact=self.request.user.id).exclude(
            id__in=QuizCard.objects.filter(quiz__completed__isnull=True).values_list('card_id', flat=True)).exclude(
            id__in=QuizCard.objects.filter(quiz__completed__gt=now - twoWeeks).values_list('card_id', flat=True))[:5]
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


class QuizAnswerViewSet(bulk_mixins.BulkCreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    """
    A ViewSet for working with quizzes.
    """
    queryset = QuizAnswer.objects.all()
    serializer_class = QuizAnswerSerializer
    ordering = ('-created',)

    @transaction.atomic
    def perform_create(self, serializer):

        serializer.save()

        quizAnswers = serializer.instance
        quiz = quizAnswers[0].quiz

        quiz.completed = timezone.now()
        quiz.save()

        for quizCard in quiz.quiz_cards.all():

            meaningModels = quizCard.card.meanings.all()
            answerModels = quizCard.quiz_answers.all()

            cardIsCorrect = len(meaningModels) == len(answerModels)
            meaningTexts = set(meaning.text.lower() for meaning in meaningModels)

            for quizAnswer in quizCard.quiz_answers.all():

                if quizAnswer.text in meaningTexts:
                    quizAnswer.is_correct = True
                else:
                    quizAnswer.is_correct = False
                    cardIsCorrect = False

                quizAnswer.save()

            if cardIsCorrect and quizCard.card.isToStudy():
                quizCard.card.to_study.delete()
                # todo move to somewhere like model.create
                isLearned = CardIsLearned()
                isLearned.user = self.request.user
                isLearned.card = quizCard.card
                isLearned.save()

            if not cardIsCorrect and quizCard.card.isLearned():
                quizCard.card.is_learned.delete()
                toStudy = CardToStudy()
                toStudy.user = self.request.user
                toStudy.card = quizCard.card
                toStudy.save()
