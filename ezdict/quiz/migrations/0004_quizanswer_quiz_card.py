# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quizanswer_is_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizanswer',
            name='quiz_card',
            field=models.OneToOneField(related_name='quiz_answer', default=None, to='quiz.QuizCard'),
            preserve_default=False,
        ),
    ]
