from rest_framework import serializers
from models import WordToLearn, WordIsLearned
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import ugettext as _


class WordToLearnSerializer(serializers.ModelSerializer):

    class Meta:
        model = WordToLearn
        validators = [
            UniqueTogetherValidator(
                queryset=WordToLearn.objects.all(),
                fields=('user', 'string'),
                message=_('You already learn this word')
            )
        ]

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    def validate_user(self, value):
        return self.context['request'].user


class WordIsLearnedSerializer(serializers.ModelSerializer):

    class Meta:
        model = WordIsLearned

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    def validate_user(self, value):
        return self.context['request'].user
