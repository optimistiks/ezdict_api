from rest_framework import serializers
from models import TranslationHistory


class TranslationHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TranslationHistory

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    count = serializers.IntegerField(read_only=True)

    def validate_user(self, value):
        return self.context['request'].user
