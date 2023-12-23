from django.urls import path
from .import views

urlpatterns = [
    path('', views.Product_list, name='products'),
    path('products/<int:pro_id>', views.product_detail, name='product'),
    path('menu/', views.menu, name='menu'),

]