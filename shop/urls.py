from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.index,         name='index'),
    path('product/<int:pk>/',       views.product_detail,name='product_detail'),
    path('cart/',                   views.cart,          name='cart'),
    path('add-to-cart/<int:pk>/',   views.add_to_cart,   name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:pk>/',   views.update_cart,   name='update_cart'),
    path('checkout/',               views.checkout,      name='checkout'),
    path('payment/<int:order_id>/', views.payment,       name='payment'),
    path('orders/',                 views.order_history, name='order_history'),
]
