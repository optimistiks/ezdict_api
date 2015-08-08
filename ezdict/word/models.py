from django.db import models
from django.conf import settings


class WordToLearn(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    string = models.CharField(max_length=255)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='word_to_learn')


class WordIsLearned(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    string = models.CharField(max_length=255)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='word_is_learned')

