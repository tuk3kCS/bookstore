"""
Author Model - Book Domain
Represents book authors in the bookstore system
"""
from django.db import models


class Author(models.Model):
    """Author model representing a book author"""
    
    name = models.CharField(max_length=100, verbose_name='Tên tác giả')
    biography = models.TextField(blank=True, null=True, verbose_name='Tiểu sử')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Ngày sinh')
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='Quốc tịch')
    image = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name='Ảnh')
    website = models.URLField(blank=True, null=True, verbose_name='Website')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'authors'
        ordering = ['name']
        verbose_name = 'Tác giả'
        verbose_name_plural = 'Tác giả'
    
    def __str__(self):
        return self.name
    
    def get_book_count(self):
        """Get total number of books by this author"""
        return self.books.count()
    
    def get_average_rating(self):
        """Get average rating of all books by this author"""
        from django.db.models import Avg
        from store.models.book.rating import Rating
        books = self.books.all()
        if books.exists():
            avg = Rating.objects.filter(book__in=books).aggregate(Avg('score'))['score__avg']
            return round(avg, 1) if avg else 0
        return 0
