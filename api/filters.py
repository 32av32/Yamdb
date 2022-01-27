from django_filters import rest_framework as filters

from api.models import Titles


class TitleFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name='name', lookup_expr='in')
    # category = filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Titles
        fields = ('name', )
        # fields = ('name', 'category')
