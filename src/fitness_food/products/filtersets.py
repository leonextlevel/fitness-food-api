from django_filters import rest_framework as filters

from fitness_food.products.models import Product


class ProductFilter(filters.FilterSet):
    product_name = filters.CharFilter(
        field_name='product_name', lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='categories__name', lookup_expr='icontains'
    )
    packaging = filters.CharFilter(
        field_name='packaging__name', lookup_expr='icontains'
    )
    brand = filters.CharFilter(
        field_name='brands__name', lookup_expr='icontains'
    )

    class Meta:
        model = Product
        fields = [
            'status',
        ]
