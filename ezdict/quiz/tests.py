from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ezdict.quiz.models import Quiz, QuizCard, QuizAnswer
from ezdict.card.models import Card, CardToStudy, CardMeaning, CardIsLearned
from django.utils import timezone
from django.conf import settings


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

    def createCardMeaning(self, user, card, text):
        cardMeaning = CardMeaning()
        cardMeaning.user = user
        cardMeaning.card = card
        cardMeaning.text = text
        cardMeaning.save()
        return cardMeaning

    def createCardToStudy(self, user, card):
        toStudy = CardToStudy()
        toStudy.card = card
        toStudy.user = user
        toStudy.save()
        return toStudy

    def createCardIsLearned(self, user, card):
        isLearned = CardIsLearned()
        isLearned.card = card
        isLearned.user = user
        isLearned.save()
        return isLearned

    def createQuiz(self, user):
        quiz = Quiz()
        quiz.user = user
        quiz.save()
        return quiz

    def createQuizCard(self, user, quiz, card):
        quizCard = QuizCard()
        quizCard.quiz = quiz
        quizCard.card = card
        quizCard.user = user
        quizCard.save()
        return quizCard

    def testQuizIsNotCreatedIfThereAreNoCardsAndErrorIsThrown(self):
        url = reverse('quiz-list')

        data = {'type': 'to_study'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testQuizIsCreatedWithSetOfQuizCards(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        data = {'type': 'to_study'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testQuizIsCreatedWithSetOfNoMoreThanNumberOfCardsInSettings(self):
        url = reverse('quiz-list')

        for x in xrange(0, settings.EZDICT['QUIZ']['CARDS_IN_QUIZ'] * 2):
            card = self.createCard(self.user, 'hello%d' % x)
            self.createCardToStudy(self.user, card)

        data = {'type': 'to_study'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), settings.EZDICT['QUIZ']['CARDS_IN_QUIZ'])

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

        data = {'type': 'to_study'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testErrorIsThrownWhenNotSpecifyingType(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        self.createCard(self.user, 'hello2')
        self.createCard(self.user, 'hello3')

        card = self.createCard(self.user, 'hello4')
        self.createCardIsLearned(self.user, card)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testOnlyCardsToStudyAreUsedWhenPassingTypeField(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        self.createCard(self.user, 'hello2')
        self.createCard(self.user, 'hello3')

        card = self.createCard(self.user, 'hello4')
        self.createCardIsLearned(self.user, card)

        data = {'type': 'to_study'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testOnlyLearnedCardsAreUsedWhenPassingTypeField(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardIsLearned(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardIsLearned(self.user, card)

        self.createCard(self.user, 'hello2')
        self.createCard(self.user, 'hello3')

        card = self.createCard(self.user, 'hello4')
        self.createCardToStudy(self.user, card)

        data = {'type': 'is_learned'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testCardCantBeInMultipleUncompletedTestsAtOnce(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)

        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        data = {'type': 'to_study'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCardCanBeInCompletedAndUncompletedTestsAtOnce(self):
        url = reverse('quiz-list')

        card = self.createCard(self.user, 'hello')
        self.createCardToStudy(self.user, card)
        card = self.createCard(self.user, 'hello1')
        self.createCardToStudy(self.user, card)

        # create test
        data = {'type': 'to_study'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        # complete test
        quizId = response.data['id']
        quiz = Quiz.objects.get(id__exact=quizId)
        quiz.completed = timezone.now() - settings.EZDICT['QUIZ']['CARD_TIMEDELTA']
        quiz.save()

        # try to create test again
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        # complete test again
        quizId = response.data['id']
        quiz = Quiz.objects.get(id__exact=quizId)
        quiz.completed = timezone.now() - settings.EZDICT['QUIZ']['CARD_TIMEDELTA']
        quiz.save()

        # try to create test again
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

    def testCardsFromCompletedQuizzesAreTakenOnlyIfGtThanTimedeltaFromSettingsIsPassed(self):
        url = reverse('quiz-list')

        # create 2 cards
        for x in xrange(0, 2):
            card = self.createCard(self.user, 'hello%d' % x)
            self.createCardToStudy(self.user, card)

        # create quiz
        data = {'type': 'to_study'}
        response = self.client.post(url, data, format='json')
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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 2)

        # create 3 more cards
        for x in xrange(0, 3):
            card = self.createCard(self.user, 'andmorehello%d' % x)
            self.createCardToStudy(self.user, card)

        # change quiz completed date
        quiz.completed = timezone.now() - settings.EZDICT['QUIZ']['CARD_TIMEDELTA']
        quiz.save()

        # create quiz (now 5 cards should be in quiz, 3 new, and 2 from the old quiz )
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('quiz_cards', response.data)
        self.assertEqual(len(response.data['quiz_cards']), 5)

    def testQuizIsCompletedAndAnswersAreMarkedAsCorrectWhenPostingASetOfCorrectAnswers(self):
        url = reverse('quiz_answer-list')

        card = self.createCard(self.user, 'hello')
        self.createCardMeaning(self.user, card, 'hello')
        self.createCardMeaning(self.user, card, 'greeting')
        self.createCardToStudy(self.user, card)

        quiz = self.createQuiz(self.user)
        quizCard = self.createQuizCard(self.user, quiz, card)

        data = [
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'hello'},
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'greeting'},
        ]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quiz.refresh_from_db()
        self.assertIsNotNone(quiz.completed)
        quizAnswers = QuizAnswer.objects.filter(quiz_card_id__exact=quizCard.id)
        self.assertEqual(quizAnswers.count(), 2)
        for quizAnswer in quizAnswers:
            self.assertTrue(quizAnswer.is_correct)

    def testQuizIsCompletedAndAnswersAreMarkedAsIncorrectWhenPostingASetOfIncorrectAnswers(self):
        url = reverse('quiz_answer-list')

        card = self.createCard(self.user, 'hello')
        self.createCardMeaning(self.user, card, 'hello')
        self.createCardMeaning(self.user, card, 'greeting')
        self.createCardToStudy(self.user, card)

        quiz = self.createQuiz(self.user)
        quizCard = self.createQuizCard(self.user, quiz, card)

        data = [
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'incorrect1'},
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'incorrect2'},
        ]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quiz.refresh_from_db()
        self.assertIsNotNone(quiz.completed)
        quizAnswers = QuizAnswer.objects.filter(quiz_card_id__exact=quizCard.id)
        self.assertEqual(quizAnswers.count(), 2)
        for quizAnswer in quizAnswers:
            self.assertFalse(quizAnswer.is_correct)

    def testCardToStudyBecomesLearnedWhenAnswersAreCorrectAndFull(self):
        url = reverse('quiz_answer-list')

        card = self.createCard(self.user, 'hello')
        self.createCardMeaning(self.user, card, 'hello')
        self.createCardMeaning(self.user, card, 'greeting')
        self.createCardToStudy(self.user, card)

        quiz = self.createQuiz(self.user)
        quizCard = self.createQuizCard(self.user, quiz, card)

        data = [
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'hello'},
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'greeting'},
        ]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quiz.refresh_from_db()
        self.assertIsNotNone(quiz.completed)
        cardToStudy = CardToStudy.objects.filter(card_id__exact=card.id).count()
        cardIsLearned = CardIsLearned.objects.filter(card_id__exact=card.id).count()
        self.assertEqual(cardToStudy, 0)
        self.assertEqual(cardIsLearned, 1)

    def testCardIsLearnedBecomesToStudyWhenAnswersAreNotCorrect(self):
        url = reverse('quiz_answer-list')

        card = self.createCard(self.user, 'hello')
        self.createCardMeaning(self.user, card, 'hello')
        self.createCardMeaning(self.user, card, 'greeting')
        self.createCardIsLearned(self.user, card)

        quiz = self.createQuiz(self.user)
        quizCard = self.createQuizCard(self.user, quiz, card)

        data = [
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'incorrect1'},
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'incorrect2'},
        ]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quiz.refresh_from_db()
        self.assertIsNotNone(quiz.completed)
        cardToStudy = CardToStudy.objects.filter(card_id__exact=card.id).count()
        cardIsLearned = CardIsLearned.objects.filter(card_id__exact=card.id).count()
        self.assertEqual(cardToStudy, 1)
        self.assertEqual(cardIsLearned, 0)

    def testCardIsLearnedBecomesToStudyWhenAnswersAreNotFull(self):
        url = reverse('quiz_answer-list')

        card = self.createCard(self.user, 'hello')
        self.createCardMeaning(self.user, card, 'hello')
        self.createCardMeaning(self.user, card, 'greeting')
        self.createCardIsLearned(self.user, card)

        quiz = self.createQuiz(self.user)
        quizCard = self.createQuizCard(self.user, quiz, card)

        data = [
            {'quiz': quiz.id, 'quiz_card': quizCard.id, 'text': 'hello'},
        ]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quiz.refresh_from_db()
        self.assertIsNotNone(quiz.completed)
        cardToStudy = CardToStudy.objects.filter(card_id__exact=card.id).count()
        cardIsLearned = CardIsLearned.objects.filter(card_id__exact=card.id).count()
        self.assertEqual(cardToStudy, 1)
        self.assertEqual(cardIsLearned, 0)
