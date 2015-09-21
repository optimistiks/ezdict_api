from django.db import models
from django.conf import settings
from django.core import serializers
from ezdict.card.models import Card


class Quiz(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quizzes')


class QuizCard(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quiz_cards')
    quiz = models.ForeignKey(Quiz, related_name='quiz_cards')
    card = models.ForeignKey(Card, related_name='quiz_cards')

    class Meta:
        unique_together = ('quiz', 'card')


class QuizAnswer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quiz_answers')
    quiz = models.ForeignKey(Quiz, related_name='quiz_answers')
    text = models.CharField(max_length=255)
