"""
Publisher Model - Book Domain
Represents book publishers in the bookstore system
"""
from django.db import models


class Publisher(models.Model):
    """Publisher model representing a book publisher"""
    
    name = models.CharField(max_length=200, unique=True, verbose_name='Tên nhà xuất bản')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    address = models.TextField(blank=True, null=True, verbose_name='Địa chỉ')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Số điện thoại')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    website = models.URLField(blank=True, null=True, verbose_name='Website')
    logo = models.ImageField(upload_to='publishers/', blank=True, null=True, verbose_name='Logo')
    founded_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Năm thành lập')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'publishers'
        ordering = ['name']
        verbose_name = 'Nhà xuất bản'
        verbose_name_plural = 'Nhà xuất bản'
    
    def __str__(self):
        return self.name
    
    def get_book_count(self):
        """Get total number of books from this publisher"""
        return self.books.count()
