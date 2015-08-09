from django.db.models.signals import pre_save
from django.dispatch import receiver
from models import TranslationHistory
from ezdict.word.models import WordToLearn
from ezdict.translation_history.models import WARN_LEVEL_5


@receiver(pre_save, sender=TranslationHistory)
def addToLearning(sender, instance, **kwargs):
    history = instance
    word = WordToLearn().findByUserAndString(history.user, history.string)
    if history.count >= WARN_LEVEL_5 and word is None:
        learning = WordToLearn()
        learning.string = history.string
        learning.user = history.user
        learning.save()
