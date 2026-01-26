"""
Order URLs - Routes for order and cart views
"""
from django.urls import path
from store.controllers.orderController import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
