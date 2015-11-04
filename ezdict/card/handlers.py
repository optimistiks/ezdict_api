from django.db.models.signals import post_save
from django.dispatch import receiver
from models import CardIsLearned
from ezdict.card.models import CardToStudy
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
