from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Lesson, Group
from .serializers import ProductSerializer, LessonSerializer
from django.utils import timezone


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(start_date__lte=timezone.now())
    serializer_class = ProductSerializer


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        user_products = user.product_set.all()
        product_name = self.kwargs.get('product_name')
        return Lesson.objects.filter(product__name=product_name, product__in=user_products)


class AccessProductViewSet(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

