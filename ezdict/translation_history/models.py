from django.db import models
from django.conf import settings

WARN_LEVEL_1 = 1
WARN_LEVEL_2 = 2
WARN_LEVEL_3 = 3
WARN_LEVEL_4 = 4
WARN_LEVEL_5 = 5


class TranslationHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    string = models.CharField(max_length=255)
    count = models.IntegerField(default=1)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='translation_history')

    def findByUserAndString(self, user, string):
        try:
            history = TranslationHistory.objects.get(user__exact=user.id,
                                                     string__exact=string)
        except TranslationHistory.DoesNotExist:
            history = None
        return history

    def warnLevel(self):
        if self.count >= WARN_LEVEL_5:
            return 5
        if self.count >= WARN_LEVEL_4:
            return 4
        if self.count >= WARN_LEVEL_3:
            return 3
        if self.count >= WARN_LEVEL_2:
            return 2
        if self.count >= WARN_LEVEL_1:
            return 1
