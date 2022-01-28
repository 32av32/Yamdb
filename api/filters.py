from django_filters import rest_framework as filters

from api.models import Titles


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')

    class Meta:
        model = Titles
        fields = ('year', )
