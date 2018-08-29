from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
# Create your views here.


@authentication_classes([])
@permission_classes([])
class OrderAPIView(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
