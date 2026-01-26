"""
Book Model - Book Domain
Represents a book in the bookstore system
"""
from django.db import models


class Book(models.Model):
    """Book model representing a book in the store"""
    
    title = models.CharField(max_length=200, verbose_name='Tên sách')
    author = models.CharField(max_length=100, verbose_name='Tác giả')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Giá')
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Số lượng trong kho')
    image = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name='Ảnh bìa')
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='Danh mục')
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True, verbose_name='ISBN')
    publisher = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nhà xuất bản')
    publication_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Năm xuất bản')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'books'
        ordering = ['-created_at']
        verbose_name = 'Sách'
        verbose_name_plural = 'Sách'
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def is_in_stock(self):
        """Check if book is in stock"""
        return self.stock_quantity > 0
    
    def get_average_rating(self):
        """Get average rating for this book"""
        from store.models.book.rating import Rating
        ratings = Rating.objects.filter(book=self)
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('score'))['score__avg'], 1)
        return 0
    
    def get_rating_count(self):
        """Get total number of ratings"""
        from store.models.book.rating import Rating
        return Rating.objects.filter(book=self).count()
