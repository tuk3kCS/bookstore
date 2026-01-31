"""
Payment Model - Order Domain
Represents payment methods available in the system
"""
from django.db import models


class Payment(models.Model):
    """Payment model for payment methods"""
    
    method_name = models.CharField(max_length=100, verbose_name='Phương thức thanh toán')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    class Meta:
        db_table = 'payments'
        ordering = ['method_name']
        verbose_name = 'Phương thức thanh toán'
        verbose_name_plural = 'Phương thức thanh toán'
    
    def __str__(self):
        return self.method_name
