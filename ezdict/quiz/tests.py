from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ezdict.quiz.models import Quiz


class QuizTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com', password='test')
        self.client.force_authenticate(user=self.user)

    def testQuizIsCreated(self):
        url = reverse('quiz-list')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
