from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Product, Lesson, Group
from .serializers import ProductSerializer, LessonSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Lesson.objects.filter(product_id=product_id)


class AccessProductView(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        groups = product.groups.all().prefetch_related('users')
        if groups.exists():
            group = groups.order_by('users').first()
            if group.users.count() < product.max_users_per_group:
                group.users.add(user)
                return Response("user added to the group", status=status.HTTP_200_OK)
            else:
                return Response("group is full", status=status.HTTP_400_BAD_REQUEST)
        else:
            if product.min_users_per_group <= 1:
                group = Group.objects.create(product=product, name="Group 1")
                group.users.add(user)
                return Response("user added to the group", status=status.HTTP_200_OK)
            else:
                return Response("group didn't create", status=status.HTTP_400_BAD_REQUEST)
