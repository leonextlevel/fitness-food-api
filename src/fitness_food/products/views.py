from rest_framework.viewsets import ModelViewSet

from fitness_food.products.filtersets import ProductFilter
from fitness_food.products.models import Product
from fitness_food.products.serializers import ProductModelSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.order_by('product_name').distinct()
    serializer_class = ProductModelSerializer
    filterset_class = ProductFilter
    http_method_names = ['get']
    lookup_field = 'code'
    lookup_url_kwarg = 'code'
