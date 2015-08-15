# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def createProfiles(apps, schema_editor):
    User = apps.get_model("ezdict_api", "MyUser")
    UserProfile = apps.get_model("user_profile", "UserProfile")
    for user in User.objects.all():
        try:
            UserProfile.objects.get(user__exact=user.id)
        except UserProfile.DoesNotExist:
            profile = UserProfile()
            profile.user = user
            profile.save()


class Migration(migrations.Migration):
    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(createProfiles),
    ]
