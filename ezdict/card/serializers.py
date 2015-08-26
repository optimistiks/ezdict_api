from rest_framework import serializers
from models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    def validate_user(self, value):
        return self.context['request'].user
