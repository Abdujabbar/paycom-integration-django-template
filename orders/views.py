from .models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.viewsets import ModelViewSet
# Create your views here.


@authentication_classes([])
@permission_classes([])
class OrderAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
