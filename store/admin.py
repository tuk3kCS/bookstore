"""
Django Admin Configuration
Register models for admin interface
"""
from django.contrib import admin
from store.models import (
    Book, Rating, Customer, Staff,
    Cart, CartItem, Order, OrderItem,
    Shipping, Payment
)


# Book Domain
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'stock_quantity', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    list_editable = ['price', 'stock_quantity']
    ordering = ['-created_at']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'book', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['customer__name', 'book__title']


# Customer Domain
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email', 'phone']
    ordering = ['-created_at']


# Staff Domain
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'staff_role', 'is_active', 'created_at']
    list_filter = ['staff_role', 'is_active']
    search_fields = ['name', 'email']
    list_editable = ['is_active']


# Order Domain
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['book', 'quantity']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['customer__name', 'customer__email']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['book', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_price', 'status', 'payment', 'shipping', 'created_at']
    list_filter = ['status', 'payment', 'shipping', 'created_at']
    search_fields = ['customer__name', 'customer__email', 'shipping_phone']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ['method_name', 'fee', 'estimated_days', 'is_active']
    list_editable = ['fee', 'is_active']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['method_name', 'is_active']
    list_editable = ['is_active']


# Customize admin site
admin.site.site_header = 'Bookstore Management System'
admin.site.site_title = 'Bookstore Admin'
admin.site.index_title = 'Quản trị Nhà sách'
