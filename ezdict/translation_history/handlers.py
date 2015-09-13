from django.db.models.signals import pre_save
from django.dispatch import receiver
from models import TranslationHistory
from ezdict.card.models import Card, CardToStudy, CardMeaning
from ezdict.translation_history.models import WARN_LEVEL_5
from ezdict.user_profile.models import UserProfile
from ezdict.translation.flat_meanings import getFlatMeanings
from django.db import transaction


@receiver(pre_save, sender=TranslationHistory)
@transaction.atomic
def addToLearning(sender, instance, **kwargs):
    history = instance
    card = Card().findByUserAndText(history.user, history.string)
    if history.count >= WARN_LEVEL_5:
        if card is None:
            card = Card()
            card.text = history.string
            card.user = history.user
            card.save()
            profile = UserProfile().findByUser(card.user)
            meanings = getFlatMeanings(card.text, profile.target_lang)
            for meaning in meanings:
                cardMeaning = CardMeaning()
                cardMeaning.text = meaning
                cardMeaning.card = card
                cardMeaning.user = card.user
                cardMeaning.save()
        try:
            card.to_study
        except CardToStudy.DoesNotExist:
            cardToStudy = CardToStudy()
            cardToStudy.card = card
            cardToStudy.user = card.user
            cardToStudy.save()
