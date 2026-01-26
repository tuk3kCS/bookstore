"""
Customer URLs - Routes for customer-related views
"""
from django.urls import path
from store.controllers.customerController import views

urlpatterns = [
    path('register/', views.customer_register, name='customer_register'),
    path('login/', views.customer_login, name='customer_login'),
    path('logout/', views.customer_logout, name='customer_logout'),
    path('profile/', views.customer_profile, name='customer_profile'),
]
