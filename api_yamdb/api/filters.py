from django_filters import rest_framework as filters
from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(lookup_expr='slug')
    category = filters.CharFilter(lookup_expr='slug')
    name = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']
