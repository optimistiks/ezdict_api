from rest_framework import serializers
from models import Card
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import ugettext as _


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

    def validate_user(self, value):
        return self.context['request'].user
