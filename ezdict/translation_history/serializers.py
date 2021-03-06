from rest_framework import serializers
from models import TranslationHistory


class TranslationHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TranslationHistory

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    warn_level = serializers.SerializerMethodField(read_only=True)

    def get_warn_level(self, obj):
        return obj.warnLevel()

    def validate_user(self, value):
        return self.context['request'].user

    def update(self, instance, validated_data):
        instance.count += 1
        instance.save()
        return instance
