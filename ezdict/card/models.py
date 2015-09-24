from django.db import models
from django.conf import settings
from django.core import serializers
import json


class Card(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=255)
    article = models.TextField(blank=True, default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cards')

    class Meta:
        unique_together = ('user', 'text')

    def findByUserAndText(self, user, text):
        try:
            card = Card.objects.get(user__exact=user.id,
                                    text__exact=text)
        except self.DoesNotExist:
            card = None
        return card

    def isToStudy(self):
        isToStudy = True
        try:
            self.to_study
        except CardToStudy.DoesNotExist:
            isToStudy = False
        return isToStudy

    def isLearned(self):
        isLearned = True
        try:
            self.is_learned
        except CardIsLearned.DoesNotExist:
            isLearned = False
        return isLearned

    def __str__(self):
        data = serializers.serialize('json', [self, ])
        struct = json.loads(data)
        data = json.dumps(struct[0])
        return data


class CardMeaning(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='meanings')
    card = models.ForeignKey(Card, related_name='meanings')

    class Meta:
        unique_together = ('card', 'text')

    def findAllByCardAndText(self, card, text):
        try:
            cards = Card.objects.all(card__exact=card.id,
                                     text__exact=text)
        except self.DoesNotExist:
            cards = None
        return cards


class CardToStudy(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_studies')
    card = models.OneToOneField(Card, related_name='to_study')

    class Meta:
        unique_together = ('user', 'card')

    def find_by_user_and_card(self, user, card):
        try:
            toStudy = CardToStudy.objects.get(user__exact=user.id,
                                              card__exact=card.id)
        except self.DoesNotExist:
            toStudy = None
        return toStudy


class CardIsLearned(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='learned_cards')
    card = models.OneToOneField(Card, related_name='is_learned')

    class Meta:
        unique_together = ('user', 'card')

    def find_by_user_and_card(self, user, card):
        try:
            isLearned = CardIsLearned.objects.get(user__exact=user.id,
                                                  card__exact=card.id)
        except self.DoesNotExist:
            isLearned = None
        return isLearned
