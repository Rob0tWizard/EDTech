from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('lessons/<int:product_id>/', views.LessonListView.as_view(), name='lesson-list'),
    path('access-product/', views.AccessProductView.as_view(), name='access-product'),
]