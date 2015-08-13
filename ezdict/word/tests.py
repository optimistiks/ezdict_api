from django.test import TestCase
from ezdict.word.models import WordToLearn
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class WordTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com', password='test')

    def test_same_word_cannot_be_added_to_learning_twice(self):
        word = WordToLearn()
        word.string = 'hello'
        word.user = self.user
        word.save()
        self.assertGreater(word.id, 0)
        word = WordToLearn()
        word.string = 'hello'
        word.user = self.user
        self.assertRaises(ValidationError, word.validate_unique)
