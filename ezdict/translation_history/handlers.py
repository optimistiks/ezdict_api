from django.db.models.signals import pre_save
from django.dispatch import receiver
from models import TranslationHistory
from ezdict.card.models import Card, CardToStudy
from ezdict.translation_history.models import WARN_LEVEL_5


@receiver(pre_save, sender=TranslationHistory)
def addToLearning(sender, instance, **kwargs):
    history = instance
    card = Card().findByUserAndText(history.user, history.string)
    if history.count >= WARN_LEVEL_5:
        if card is None:
            card = Card()
            card.text = history.string
            card.user = history.user
            card.save()
        if card.card_to_study is None:
            cardToStudy = CardToStudy()
            cardToStudy.card = card
            cardToStudy.user = card.user
            cardToStudy.save()
