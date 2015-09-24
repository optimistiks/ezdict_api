from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ezdict.quiz.models import Quiz, QuizCard, QuizAnswer
from ezdict.card.models import Card, CardToStudy, CardMeaning, CardIsLearned
from django.utils import timezone
import datetime


class CardTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='cardtest', email='cardtest@cardtest.com', password='card')
        self.client.force_authenticate(user=self.user)

    def testCardIsLearnedIsDeletedWhenCardToStudyIsCreated(self):
        card = Card()
        card.user = self.user
        card.text = 'hello'
        card.save()

        is_learned = CardIsLearned()
        is_learned.user = self.user
        is_learned.card = card
        is_learned.save()

        to_study = CardToStudy()
        to_study.user = self.user
        to_study.card = card
        to_study.save()

        is_learned = CardIsLearned().find_by_user_and_card(self.user, card)
        self.assertIsNone(is_learned)

    def testCardToStudyIsDeletedWhenCardIsLearnedIsCreated(self):
        card = Card()
        card.user = self.user
        card.text = 'hello'
        card.save()

        to_study = CardToStudy()
        to_study.user = self.user
        to_study.card = card
        to_study.save()

        is_learned = CardIsLearned()
        is_learned.user = self.user
        is_learned.card = card
        is_learned.save()

        to_study = CardToStudy().find_by_user_and_card(self.user, card)
        self.assertIsNone(to_study)
