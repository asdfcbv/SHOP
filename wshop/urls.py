from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    # Категория → список товаров
    path('category/<int:category_id>/', products_by_category, name='products_by_category'),
    # Товар → детальная страница
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
]