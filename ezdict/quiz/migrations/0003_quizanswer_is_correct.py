# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20150921_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizanswer',
            name='is_correct',
            field=models.NullBooleanField(),
        ),
    ]
