from django.dispatch import receiver
from djoser.signals import user_registered
from models import UserProfile


@receiver(user_registered)
def createProfile(sender, user, request, **kwargs):
    profile = UserProfile()
    profile.user = user
    profile.save()
