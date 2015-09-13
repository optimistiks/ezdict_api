from django.test import TestCase
from models import TranslationHistory, WARN_LEVEL_5
from ezdict.card.models import Card
from django.contrib.auth import get_user_model
from ezdict.user_profile.models import UserProfile


class TranslationHistoryTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com', password='test')
        profile = UserProfile()
        profile.user = self.user
        profile.target_lang = 'ru'
        profile.save()

    def test_card_is_created_on_signal_and_added_to_study(self):
        card = Card().findByUserAndText(self.user, 'hello5')
        self.assertIsNone(card)
        history = TranslationHistory()
        history.user = self.user
        history.string = 'hello5'
        history.count = WARN_LEVEL_5
        history.save()
        card = Card().findByUserAndText(self.user, 'hello5')
        self.assertIsNotNone(card)
        self.assertIsNotNone(card.to_study)

    def test_card_is_not_created_on_signal(self):
        card = Card().findByUserAndText(self.user, 'hello1')
        self.assertIsNone(card)
        history = TranslationHistory()
        history.user = self.user
        history.string = 'hello1'
        history.count = 1
        history.save()
        card = Card().findByUserAndText(self.user, 'hello1')
        self.assertIsNone(card)
