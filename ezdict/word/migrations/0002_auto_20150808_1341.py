# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from ezdict.translation_history.models import WARN_LEVEL_5


def process_history(apps, schema_editor):
    History = apps.get_model("translation_history", "TranslationHistory")
    WordToLearn = apps.get_model("word", "WordToLearn")
    for history in History.objects.all():
        if history.count >= WARN_LEVEL_5:
            learning = WordToLearn()
            learning.string = history.string
            learning.user = history.user
            learning.save()


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(process_history),
    ]
