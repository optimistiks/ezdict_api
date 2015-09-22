from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ezdict.quiz.models import Quiz
from ezdict.card.models import Card, CardToStudy
from django.utils import timezone
import datetime


class QuizTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com', password='test')
        self.client.force_authenticate(user=self.user)

    def createCard(self, user, text):
        card = Card()
        card.user = user
        card.text = text
        card.save()
        return card

    def createCardToStudy(self, user, card):
        toStudy = CardToStudy()
        toStudy.card = card
        toStudy.user = user
        toStudy.save()
        return toStudy

    def testQuizIsNotCreatedIfThereAreNoCardsAndErrorIsThrown(self):
        url = reverse('quiz-list')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testQuizIsCreatedWithSetOfQuizCards(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testQuizIsCreatedWithSetOfNoMoreThan5Cards(self):
        url = reverse('quiz-list')

        for x in xrange(0, 10):
            card = self.createCard(self.user, 'hello%d' % x)
            self.createCardToStudy(self.user, card)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 5)

    def testOnlyCardsOfCurrentUserAreUsed(self):
        url = reverse('quiz-list')

        anotherUser = get_user_model().objects.create_user(
            username='test1', email='test1@test.com', password='test1')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        card = self.createCard(anotherUser, 'hello')
        self.createCardToStudy(anotherUser, card)
        card = self.createCard(anotherUser, 'hello1')
        self.createCardToStudy(anotherUser, card)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testOnlyCardsToStudyAreUsed(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        self.createCard(self.user, 'hello2')
        self.createCard(self.user, 'hello3')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testCardCantBeInMultipleUncompletedTestsAtOnce(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)

        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCardCanBeInCompletedAndUncompletedTestsAtOnce(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        # create test
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        # complete test
        quizId = response.data['id']
        quiz = Quiz.objects.get(id__exact=quizId)
        quiz.completed = timezone.now() - datetime.timedelta(weeks=2)
        quiz.save()

        # try to create test again
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        # complete test again
        quizId = response.data['id']
        quiz = Quiz.objects.get(id__exact=quizId)
        quiz.completed = timezone.now() - datetime.timedelta(weeks=2)
        quiz.save()

        # try to create test again
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testCardsFromCompletedQuizzesAreTakenOnlyIfGtThanTwoWeeksPassed(self):
        url = reverse('quiz-list')

        # create 2 cards
        for x in xrange(0, 2):
            card = self.createCard(self.user, 'hello%d' % x)
            self.createCardToStudy(self.user, card)

        # create quiz
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        # complete quiz
        quizId = response.data['id']
        quiz = Quiz.objects.get(id__exact=quizId)
        quiz.completed = timezone.now()
        quiz.save()

        # create 2 more cards
        for x in xrange(0, 2):
            card = self.createCard(self.user, 'morehello%d' % x)
            self.createCardToStudy(self.user, card)

        # create quiz (now only 2 cards should get to quiz because quiz with other 2 is recently completed )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        # create 3 more cards
        for x in xrange(0, 3):
            card = self.createCard(self.user, 'andmorehello%d' % x)
            self.createCardToStudy(self.user, card)

        # change quiz completed date
        quiz.completed = timezone.now() - datetime.timedelta(weeks=2)
        quiz.save()

        # create quiz (now 5 cards should be in quiz, 3 new, and 2 from the old quiz )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 5)
