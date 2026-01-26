"""
Customer Model - Customer Domain
Represents a customer in the bookstore system
"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Customer(models.Model):
    """Customer model representing a registered customer"""
    
    name = models.CharField(max_length=100, verbose_name='Họ tên')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=128, verbose_name='Mật khẩu')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Số điện thoại')
    address = models.TextField(blank=True, null=True, verbose_name='Địa chỉ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đăng ký')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']
        verbose_name = 'Khách hàng'
        verbose_name_plural = 'Khách hàng'
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password matches"""
        return check_password(raw_password, self.password)
    
    def get_active_cart(self):
        """Get or create active cart for customer"""
        from store.models.order.cart import Cart
        cart, created = Cart.objects.get_or_create(
            customer=self,
            is_active=True
        )
        return cart
