from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from models import CardIsLearned, CardToStudy
from ezdict.card.models import Card, CardToStudy, CardMeaning
from ezdict.translation_history.models import WARN_LEVEL_5
from ezdict.user_profile.models import UserProfile
from ezdict.translation.flat_meanings import getFlatMeanings
from django.db import transaction


@receiver(post_save, sender=CardIsLearned)
@transaction.atomic
def remove_card_to_study(sender, instance, **kwargs):
    to_study = CardToStudy().find_by_user_and_card(instance.user, instance.card)
    if to_study is not None:
        to_study.delete()


@receiver(post_save, sender=CardToStudy)
@transaction.atomic
def remove_card_is_learned(sender, instance, **kwargs):
    is_learned = CardIsLearned().find_by_user_and_card(instance.user, instance.card)
    if is_learned is not None:
        is_learned.delete()
