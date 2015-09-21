from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ezdict.quiz.models import Quiz
from ezdict.card.models import Card, CardToStudy


class QuizTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com', password='test')
        self.client.force_authenticate(user=self.user)

    def testQuizIsNotCreatedIfThereAreNoCardsAndErrorIsThrown(self):
        url = reverse('quiz-list')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testQuizIsCreatedWithSetOfQuizCards(self):
        url = reverse('quiz-list')

        card = Card()
        card.user = self.user
        card.text = 'hello'
        card.save()

        toStudy = CardToStudy()
        toStudy.card = card
        toStudy.user = self.user
        toStudy.save()

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.quiz_cards)

