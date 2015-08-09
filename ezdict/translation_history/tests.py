from django.test import TestCase
from models import TranslationHistory, WARN_LEVEL_5
from ezdict.word.models import WordToLearn
from django.contrib.auth import get_user_model


class TranslationHistoryTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com', password='test')

    def test_word_is_created_on_signal(self):
        history = TranslationHistory()
        history.user = self.user
        history.string = 'hello5'
        history.count = WARN_LEVEL_5
        history.save()
        word = WordToLearn().findByUserAndString(self.user, 'hello5')
        self.assertIsNotNone(word)

    def test_word_is_not_created_on_signal(self):
        history = TranslationHistory()
        history.user = self.user
        history.string = 'hello1'
        history.count = 1
        history.save()
        word = WordToLearn().findByUserAndString(self.user, 'hello1')
        self.assertIsNone(word)
