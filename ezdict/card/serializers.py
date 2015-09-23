from rest_framework import serializers
from models import Card, CardMeaning, CardToStudy, CardIsLearned
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import ugettext as _
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)
from rest_framework.exceptions import PermissionDenied


class CardToStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = CardToStudy
        validators = [
            UniqueTogetherValidator(
                queryset=CardToStudy.objects.all(),
                fields=('user', 'card'),
                message=_('This card is already being studied.')
            )
        ]

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), default=None)

    def validate_user(self, value):
        return self.context['request'].user

    def validate_card(self, value):
        if value.user.id != self.context['request'].user.id:
            raise PermissionDenied()
        return value


class CardIsLearnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardIsLearned
        validators = [
            UniqueTogetherValidator(
                queryset=CardIsLearned.objects.all(),
                fields=('user', 'card'),
                message=_('This card is already learned.')
            )
        ]

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), default=None)

    def validate_user(self, value):
        return self.context['request'].user

    def validate_card(self, value):
        if value.user.id != self.context['request'].user.id:
            raise PermissionDenied()
        return value


class CardMeaningSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CardMeaning
        list_serializer_class = BulkListSerializer
        validators = [
            UniqueTogetherValidator(
                queryset=CardMeaning.objects.all(),
                fields=('card', 'text'),
                message=_('This meaning already exists.')
            )
        ]

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), default=None)

    def validate_user(self, value):
        return self.context['request'].user

    def validate_card(self, value):
        if value.user.id != self.context['request'].user.id:
            raise PermissionDenied()
        return value


class CardWithoutRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        validators = [
            UniqueTogetherValidator(
                queryset=Card.objects.all(),
                fields=('user', 'text'),
                message=_('Card for this text already exists.')
            )
        ]

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    meanings = CardMeaningSerializer(read_only=True, many=True)
    to_study = CardToStudySerializer(read_only=True)
    is_learned = CardIsLearnedSerializer(read_only=True)

    def validate_user(self, value):
        return self.context['request'].user
