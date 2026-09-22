from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('add_product/', views.add_product, name='add_product'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/remove/<int:item_id>', views.remove_cart, name='remove_cart'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
