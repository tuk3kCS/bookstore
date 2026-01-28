"""
Category Model - Book Domain
Represents book categories in the bookstore system
"""
from django.db import models


class Category(models.Model):
    """Category model representing a book category"""
    
    name = models.CharField(max_length=100, unique=True, verbose_name='Tên danh mục')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Danh mục cha'
    )
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
    
    def __str__(self):
        return self.name
    
    def get_full_path(self):
        """Get full category path (e.g., 'Văn học > Tiểu thuyết')"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name
    
    def get_book_count(self):
        """Get total number of books in this category"""
        return self.books.count()
