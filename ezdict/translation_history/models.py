from django.db import models
from django.conf import settings


class TranslationHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    string = models.CharField(max_length=255)
    count = models.IntegerField(default=1)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='translation_history')
