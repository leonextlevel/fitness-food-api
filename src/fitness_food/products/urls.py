from rest_framework import routers

from fitness_food.products.views import ProductModelViewSet

router = routers.SimpleRouter()
router.register(r'', ProductModelViewSet)


urlpatterns = []

urlpatterns += router.urls
