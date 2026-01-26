"""
Book URLs - Routes for book-related views
"""
from django.urls import path
from store.controllers.bookController import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/search/', views.book_search, name='book_search'),
    path('books/<int:book_id>/rate/', views.book_rate, name='book_rate'),
]
