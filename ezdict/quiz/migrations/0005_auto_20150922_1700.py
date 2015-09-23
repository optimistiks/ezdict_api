# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quizanswer_quiz_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizanswer',
            name='quiz_card',
            field=models.ForeignKey(related_name='quiz_answers', to='quiz.QuizCard'),
        ),
    ]
