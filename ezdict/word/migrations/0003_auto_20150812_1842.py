# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def prepareWords(apps, schema_editor):
    WordToLearn = apps.get_model("word", "WordToLearn")
    for word in WordToLearn.objects.all():
        if WordToLearn.objects.filter(string=word.string).count() > 1:
            word.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('word', '0002_auto_20150808_1341'),
    ]

    operations = [
        migrations.RunPython(prepareWords),
    ]
