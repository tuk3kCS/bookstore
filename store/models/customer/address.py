"""
Address Model - Customer Domain
Represents customer shipping addresses
"""
from django.db import models


class Address(models.Model):
    """Address model representing a customer's shipping address"""
    
    customer = models.ForeignKey(
        'store.Customer',
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Khách hàng'
    )
    recipient_name = models.CharField(max_length=100, verbose_name='Tên người nhận')
    phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    province = models.CharField(max_length=100, verbose_name='Tỉnh/Thành phố')
    district = models.CharField(max_length=100, verbose_name='Quận/Huyện')
    ward = models.CharField(max_length=100, verbose_name='Phường/Xã')
    street_address = models.TextField(verbose_name='Địa chỉ chi tiết')
    is_default = models.BooleanField(default=False, verbose_name='Địa chỉ mặc định')
    address_type = models.CharField(
        max_length=20,
        choices=[
            ('home', 'Nhà riêng'),
            ('office', 'Văn phòng'),
            ('other', 'Khác'),
        ],
        default='home',
        verbose_name='Loại địa chỉ'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'addresses'
        ordering = ['-is_default', '-created_at']
        verbose_name = 'Địa chỉ'
        verbose_name_plural = 'Địa chỉ'
    
    def __str__(self):
        return f"{self.recipient_name} - {self.street_address}, {self.ward}, {self.district}, {self.province}"
    
    def get_full_address(self):
        """Get complete formatted address"""
        return f"{self.street_address}, {self.ward}, {self.district}, {self.province}"
    
    def save(self, *args, **kwargs):
        """Override save to ensure only one default address per customer"""
        if self.is_default:
            Address.objects.filter(customer=self.customer, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
