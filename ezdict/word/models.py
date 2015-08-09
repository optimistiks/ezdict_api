from django.db import models
from django.conf import settings


class WordToLearn(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    string = models.CharField(max_length=255)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='word_to_learn')

    def findByUserAndString(self, user, string):
        try:
            word = WordToLearn.objects.get(user__exact=user.id,
                                           string__exact=string)
        except WordToLearn.DoesNotExist:
            word = None
        return word


class WordIsLearned(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    string = models.CharField(max_length=255)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='word_is_learned')

    def findByUserAndString(self, user, string):
        try:
            word = WordIsLearned.objects.get(user__exact=user.id,
                                             string__exact=string)
        except WordIsLearned.DoesNotExist:
            word = None
        return word
