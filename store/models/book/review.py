"""
Review Model - Book Domain
Represents detailed customer reviews for books (extends Rating)
"""
from django.db import models


class Review(models.Model):
    """Review model for detailed book reviews"""
    
    customer = models.ForeignKey(
        'store.Customer',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Khách hàng'
    )
    book = models.ForeignKey(
        'store.Book',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Sách'
    )
    title = models.CharField(max_length=200, verbose_name='Tiêu đề')
    content = models.TextField(verbose_name='Nội dung đánh giá')
    pros = models.TextField(blank=True, null=True, verbose_name='Ưu điểm')
    cons = models.TextField(blank=True, null=True, verbose_name='Nhược điểm')
    is_verified_purchase = models.BooleanField(default=False, verbose_name='Mua hàng xác thực')
    helpful_count = models.PositiveIntegerField(default=0, verbose_name='Số lượt hữu ích')
    is_approved = models.BooleanField(default=True, verbose_name='Đã duyệt')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'reviews'
        ordering = ['-helpful_count', '-created_at']
        verbose_name = 'Bài đánh giá'
        verbose_name_plural = 'Bài đánh giá'
    
    def __str__(self):
        return f"{self.title} - {self.book.title}"
    
    def mark_helpful(self):
        """Increment helpful count"""
        self.helpful_count += 1
        self.save()
