from rest_framework import serializers
from models import Quiz, QuizCard, QuizAnswer
from ezdict.card.serializers import CardSerializer
from ezdict.ezdict_api.serializers import ModelWithUserSerializer
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import ugettext as _


class QuizAnswerSerializer(BulkSerializerMixin, ModelWithUserSerializer):
    class Meta:
        model = QuizAnswer
        list_serializer_class = BulkListSerializer

    def validate_quiz(self, value):
        if value.user.id != self.context['request'].user.id:
            raise PermissionDenied()
        return value

    def validate_quiz_card(self, value):
        if value.user.id != self.context['request'].user.id:
            raise PermissionDenied()
        return value


class QuizCardSerializer(ModelWithUserSerializer):
    class Meta:
        model = QuizCard

    card = CardSerializer(read_only=True, default=None)


class QuizSerializer(ModelWithUserSerializer):
    class Meta:
        model = Quiz

    completed = serializers.DateTimeField(read_only=True, default=None)
    quiz_cards = QuizCardSerializer(read_only=True, many=True)
    quiz_answers = QuizAnswerSerializer(read_only=True, many=True)

    def validate_type(self, value):
        if value != Quiz.TYPE_TO_STUDY and value != Quiz.TYPE_IS_LEARNED:
            raise serializers.ValidationError(_('Invalid parameter %(param)s.') % {'param': 'type'})
        return value
