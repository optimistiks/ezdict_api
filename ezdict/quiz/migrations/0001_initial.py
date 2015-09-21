# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0014_auto_20150913_1607'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('completed', models.DateTimeField()),
                ('user', models.ForeignKey(related_name='quizzes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=255)),
                ('quiz', models.ForeignKey(related_name='quiz_answers', to='quiz.Quiz')),
                ('user', models.ForeignKey(related_name='quiz_answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(related_name='quiz_cards', to='card.Card')),
                ('quiz', models.ForeignKey(related_name='quiz_cards', to='quiz.Quiz')),
                ('user', models.ForeignKey(related_name='quiz_cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='quizcard',
            unique_together=set([('quiz', 'card')]),
        ),
    ]
