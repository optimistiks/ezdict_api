from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_profile')
    target_lang = models.CharField(max_length=5, default='ru')

    @staticmethod
    def findByUser(user):
        try:
            profile = UserProfile.objects.get(user__exact=user.id)
        except UserProfile.DoesNotExist:
            profile = None
        return profile
