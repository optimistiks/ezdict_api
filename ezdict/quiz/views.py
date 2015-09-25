from models import Quiz, QuizCard, QuizAnswer
from ezdict.card.models import Card, CardToStudy, CardIsLearned
from serializers import QuizSerializer, QuizAnswerSerializer
from rest_framework import mixins, serializers
from rest_framework_bulk import mixins as bulk_mixins
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import ugettext as _
from django.db import transaction
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

    TYPE_TO_STUDY = 'to_study'
    TYPE_LEARNED = 'is_learned'

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
        quiz = serializer.instance

        now = timezone.now()
        twoWeeks = datetime.timedelta(weeks=2)
        cards = Card.objects

        if quiz.is_type_to_study():
            cards = cards.filter(to_study__isnull=False)

        if quiz.is_type_learned():
            cards = cards.filter(is_learned__isnull=False)

        cards = cards.filter(user_id__exact=self.request.user.id).exclude(
            id__in=QuizCard.objects.filter(quiz__completed__isnull=True).values_list('card_id', flat=True)).exclude(
            id__in=QuizCard.objects.filter(quiz__completed__gt=now - twoWeeks).values_list('card_id', flat=True))[:5]

        if cards:
            for card in cards:
                # todo: move to model.create
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
    A ViewSet for working with quiz answers.
    quiz -- a quiz to search answers for
    """
    queryset = QuizAnswer.objects.all()
    serializer_class = QuizAnswerSerializer
    filter_fields = ('quiz',)
    ordering = ('-created',)

    @transaction.atomic
    def perform_create(self, serializer):

        serializer.save()

        quiz_answers = serializer.instance
        quiz = quiz_answers[0].quiz

        quiz.completed = timezone.now()
        quiz.save()

        for quiz_card in quiz.quiz_cards.all():

            meaning_models = quiz_card.card.meanings.all()
            answer_models = quiz_card.quiz_answers.all()

            card_is_correct = len(meaning_models) == len(answer_models)
            meaning_texts = set(meaning.text.lower() for meaning in meaning_models)

            for quizAnswer in quiz_card.quiz_answers.all():

                if quizAnswer.text in meaning_texts:
                    quizAnswer.is_correct = True
                else:
                    quizAnswer.is_correct = False
                    card_is_correct = False

                quizAnswer.save()

            if card_is_correct and quiz_card.card.isToStudy():
                # todo move to somewhere like model.create
                is_learned = CardIsLearned()
                is_learned.user = self.request.user
                is_learned.card = quiz_card.card
                is_learned.save()

            if not card_is_correct and quiz_card.card.isLearned():
                to_study = CardToStudy()
                to_study.user = self.request.user
                to_study.card = quiz_card.card
                to_study.save()
