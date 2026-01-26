"""
Staff URLs - Routes for staff-related views
"""
from django.urls import path
from store.controllers.staffController import views

urlpatterns = [
    path('login/', views.staff_login, name='staff_login'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('books/', views.staff_book_list, name='staff_book_list'),
    path('books/add/', views.staff_book_add, name='staff_book_add'),
    path('books/<int:book_id>/edit/', views.staff_book_edit, name='staff_book_edit'),
    path('books/<int:book_id>/delete/', views.staff_book_delete, name='staff_book_delete'),
    path('orders/', views.staff_order_list, name='staff_order_list'),
    path('orders/<int:order_id>/', views.staff_order_detail, name='staff_order_detail'),
]
