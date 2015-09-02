from django.db import models
from django.conf import settings


class Card(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=255)
    article = models.TextField(blank=True, default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='card')

    class Meta:
        unique_together = ('user', 'text')

    def findByUserAndText(self, user, text):
        try:
            card = Card.objects.get(user__exact=user.id,
                                    text__exact=text)
        except self.DoesNotExist:
            card = None
        return card


class CardMeaning(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='card_meaning')
    card = models.ForeignKey(Card, related_name='card_meaning')

    class Meta:
        unique_together = ('card', 'text')

    def findAllByCardAndText(self, card, text):
        try:
            cards = Card.objects.all(card__exact=card.id,
                                     text__exact=text)
        except self.DoesNotExist:
            cards = None
        return cards
