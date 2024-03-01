from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Lesson, Group
from .serializers import ProductSerializer, LessonSerializer



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

        groups = product.groups.all()
        if groups.exists():
            group = groups.order_by('users').first()
            if group.users.count() < product.max_users_per_group:
                group.users.add(user)
                return Response("user added", status=status.HTTP_200_OK)
            else:
                return Response("group is full", status=status.HTTP_400_BAD_REQUEST)
        else:
            if product.min_users_per_group <= 1:
                group = Group.objects.create(product=product, name="Группа 1")
                group.users.add(user)
                return Response("user added to the group", status=status.HTTP_200_OK)
            else:
                return Response("group didn't create", status=status.HTTP_400_BAD_REQUEST)

