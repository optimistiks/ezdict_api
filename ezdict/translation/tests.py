from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ezdict.translation_history.models import TranslationHistory


class TranslationTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com', password='test')
        self.client.force_authenticate(user=self.user)

    def assertHistory(self, string, count):
        history = TranslationHistory().findByUserAndString(self.user, string)
        self.assertEqual(history.count, count)

    def testStringNormalizing(self):
        url = reverse('translation')

        string = 'hello'
        stringWhiteSpace = ' hello '
        stringMixedCase = 'hElLo'

        response = self.client.get(url, {'string': string})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertHistory(string, 1)

        response = self.client.get(url, {'string': stringWhiteSpace})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertHistory(string, 2)

        response = self.client.get(url, {'string': stringMixedCase})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertHistory(string, 3)

