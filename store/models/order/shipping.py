"""
Shipping Model - Order Domain
Represents shipping methods available in the system
"""
from django.db import models


class Shipping(models.Model):
    """Shipping model for delivery methods"""
    
    method_name = models.CharField(max_length=100, verbose_name='Phương thức giao hàng')
    fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Phí giao hàng')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    estimated_days = models.PositiveIntegerField(default=3, verbose_name='Số ngày dự kiến')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    class Meta:
        db_table = 'shippings'
        ordering = ['fee']
        verbose_name = 'Phương thức giao hàng'
        verbose_name_plural = 'Phương thức giao hàng'
    
    def __str__(self):
        return f"{self.method_name} - {self.fee:,.0f}đ"
