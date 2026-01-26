"""
Rating Model - Book Domain
Represents customer ratings for books
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    """Rating model for book reviews"""
    
    customer = models.ForeignKey(
        'store.Customer',
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='Khách hàng'
    )
    book = models.ForeignKey(
        'store.Book',
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='Sách'
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Điểm đánh giá'
    )
    comment = models.TextField(blank=True, null=True, verbose_name='Bình luận')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đánh giá')
    
    class Meta:
        db_table = 'ratings'
        unique_together = ['customer', 'book']  # One rating per customer per book
        ordering = ['-created_at']
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'
    
    def __str__(self):
        return f"{self.customer.name} - {self.book.title}: {self.score}/5"
