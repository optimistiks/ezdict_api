from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class UserProfileTest(APITestCase):
    def testUserProfileIsCreatedAfterRegistration(self):
        regUrl = reverse('register')
        profileUrl = reverse('user_profile')

        userResponse = self.client.post(regUrl, {'username': 'profiletest', 'email': 'profiletest@mail.ru',
                                                 'password': 'profiletest'})
        self.assertEqual(userResponse.status_code, status.HTTP_201_CREATED)

        userModel = get_user_model().objects.get(username__exact='profiletest')
        self.client.force_authenticate(user=userModel)

        profileResponse = self.client.get(profileUrl)
        self.assertEqual(profileResponse.status_code, status.HTTP_200_OK)
        self.assertEquals(profileResponse.data['user'], userResponse.data['id'])
        self.assertEquals(profileResponse.data['target_lang'], 'ru')
