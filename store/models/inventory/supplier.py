"""
Supplier Model - Inventory Domain
Represents book suppliers in the bookstore system
"""
from django.db import models


class Supplier(models.Model):
    """Supplier model representing a book supplier"""
    
    name = models.CharField(max_length=200, unique=True, verbose_name='Tên nhà cung cấp')
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name='Người liên hệ')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Số điện thoại')
    address = models.TextField(blank=True, null=True, verbose_name='Địa chỉ')
    tax_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Mã số thuế')
    bank_account = models.CharField(max_length=50, blank=True, null=True, verbose_name='Số tài khoản ngân hàng')
    bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tên ngân hàng')
    payment_terms = models.TextField(blank=True, null=True, verbose_name='Điều khoản thanh toán')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'suppliers'
        ordering = ['name']
        verbose_name = 'Nhà cung cấp'
        verbose_name_plural = 'Nhà cung cấp'
    
    def __str__(self):
        return self.name
    
    def get_total_transactions(self):
        """Get total number of inventory transactions"""
        return self.inventory_transactions.count()
    
    def get_total_amount(self):
        """Get total amount of all transactions"""
        from django.db.models import Sum
        result = self.inventory_transactions.aggregate(Sum('total_amount'))
        return result['total_amount__sum'] or 0
