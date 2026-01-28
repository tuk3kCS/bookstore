"""
Wishlist and WishlistItem Models - Customer Domain
Represents customer wishlist functionality
"""
from django.db import models


class Wishlist(models.Model):
    """Wishlist model representing a customer's wishlist"""
    
    customer = models.ForeignKey(
        'store.Customer',
        on_delete=models.CASCADE,
        related_name='wishlists',
        verbose_name='Khách hàng'
    )
    name = models.CharField(max_length=100, default='Danh sách yêu thích', verbose_name='Tên danh sách')
    is_public = models.BooleanField(default=False, verbose_name='Công khai')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'wishlists'
        ordering = ['-created_at']
        verbose_name = 'Danh sách yêu thích'
        verbose_name_plural = 'Danh sách yêu thích'
    
    def __str__(self):
        return f"{self.name} - {self.customer.name}"
    
    def get_item_count(self):
        """Get total number of items in wishlist"""
        return self.items.count()
    
    def get_total_value(self):
        """Get total value of all items in wishlist"""
        return sum(item.book.price for item in self.items.all())


class WishlistItem(models.Model):
    """WishlistItem model representing an item in a wishlist"""
    
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Danh sách yêu thích'
    )
    book = models.ForeignKey(
        'store.Book',
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        verbose_name='Sách'
    )
    priority = models.PositiveIntegerField(
        default=0,
        choices=[
            (0, 'Bình thường'),
            (1, 'Cao'),
            (2, 'Rất cao'),
        ],
        verbose_name='Độ ưu tiên'
    )
    note = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày thêm')
    
    class Meta:
        db_table = 'wishlist_items'
        unique_together = ['wishlist', 'book']
        ordering = ['-priority', '-added_at']
        verbose_name = 'Sách trong danh sách yêu thích'
        verbose_name_plural = 'Sách trong danh sách yêu thích'
    
    def __str__(self):
        return f"{self.book.title} - {self.wishlist.name}"
