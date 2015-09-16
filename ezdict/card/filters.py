from django_filters import FilterSet
from ezdict.ezdict_api.filters import ListFilter
from models import Card, CardMeaning
from django_filters import Filter
from django import forms


class InverseBooleanFilter(Filter):
    field_class = forms.NullBooleanField

    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{self.name: not value})
        return qs


class CardFilterSet(FilterSet):
    to_study = InverseBooleanFilter(name="to_study__isnull")

    class Meta:
        model = Card
        fields = ['text', 'to_study']


class CardMeaningFilterSet(FilterSet):
    """
    A filter set to allow filtering CardMeanings by multiple ids
    for batch operations
    """
    id = ListFilter(name='id')

    class Meta:
        model = CardMeaning
        fields = ['id', 'card']
