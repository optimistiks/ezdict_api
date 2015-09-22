from rest_framework import serializers
from models import Quiz, QuizCard, QuizAnswer
from ezdict.card.serializers import CardWithoutRelationsSerializer
from ezdict.ezdict_api.serializers import ModelWithUserSerializer
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import ugettext as _
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)
from rest_framework.exceptions import PermissionDenied


class QuizAnswerSerializer(ModelWithUserSerializer):
    class Meta:
        model = QuizAnswer


class QuizCardSerializer(ModelWithUserSerializer):
    class Meta:
        model = QuizCard

    card = CardWithoutRelationsSerializer(read_only=True, default=None)


class QuizSerializer(ModelWithUserSerializer):
    class Meta:
        model = Quiz

    completed = serializers.DateTimeField(read_only=True, default=None)
    quiz_cards = QuizCardSerializer(read_only=True, many=True)
