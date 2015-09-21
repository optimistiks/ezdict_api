from rest_framework import serializers
from models import Quiz, QuizCard

from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import ugettext as _
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)
from rest_framework.exceptions import PermissionDenied


class QuizCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    card = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    def validate_user(self, value):
        return self.context['request'].user


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    quiz_cards = QuizCardSerializer(read_only=True, many=True)


    def validate_user(self, value):
        return self.context['request'].user
