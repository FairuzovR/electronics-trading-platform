from django_filters import rest_framework as filters
from .models import SupplierNode


class SupplierNodeFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='country', lookup_expr='icontains')

    class Meta:
        model = SupplierNode
        fields = ['country']
