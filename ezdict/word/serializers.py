from rest_framework import serializers
from models import WordToLearn, WordIsLearned


class WordToLearnSerializer(serializers.ModelSerializer):

    class Meta:
        model = WordToLearn

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    def validate_user(self, value):
        return self.context['request'].user


class WordIsLearnedSerializer(serializers.ModelSerializer):

    class Meta:
        model = WordIsLearned

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    def validate_user(self, value):
        return self.context['request'].user
