from rest_framework import serializers
from .models import Product, Lesson, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProductSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'creator', 'name', 'start_date', 'cost', 'min_users_per_group', 'max_users_per_group']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'product', 'name', 'video_link']


class GroupSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'product', 'name', 'min_users', 'max_users', 'users']
