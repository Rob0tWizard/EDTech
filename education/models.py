from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    cost = models.DecimalField(max_digits=9, decimal_places=2)
    min_users_per_group = models.IntegerField(default=1)
    max_users_per_group = models.IntegerField(default=10)

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=100)
    video_link = models.URLField()

class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='groups')
