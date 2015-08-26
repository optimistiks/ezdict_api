from django.db import models
from django.conf import settings


class Card(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=255)
    article = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='card')

    def findByUserAndText(self, user, text):
        try:
            card = self.objects.get(user__exact=user.id,
                                    text__exact=text)
        except self.DoesNotExist:
            card = None
        return card
