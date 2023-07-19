from django.urls import include, path
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
from rest_framework.views import APIView

from fitness_food.swagger import SwaggerView


class RootView(APIView):
    def get(self, *args, **kwargs) -> Response:
        """
        API to root message endpoint.
        """
        return Response({'message': 'Fullstack Challenge 20201026'})


urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path(
        'openapi/',
        get_schema_view(title='Documentação - Fitness Food API'),
        name='openapi-schema',
    ),
    path('swagger/', SwaggerView.as_view(), name='swagger-ui'),
    path('products/', include('fitness_food.products.urls')),
]
