from .views import OrderAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'^', OrderAPIView, 'orders')

urlpatterns = router.urls
