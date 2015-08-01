from rest_framework import serializers
from ezdict.translation_history.serializers import TranslationHistorySerializer


class TranslationSerializer(serializers.Serializer):
    translation_history = TranslationHistorySerializer()
    translation = serializers.CharField()
    ya_dict = serializers.DictField()
