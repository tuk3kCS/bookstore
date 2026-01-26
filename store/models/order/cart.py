"""
Cart and CartItem Models - Order Domain
Represents shopping cart functionality
"""
from django.db import models


class Cart(models.Model):
    """Cart model representing a shopping cart"""
    
    customer = models.ForeignKey(
        'store.Customer',
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Khách hàng'
    )
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'
    
    def __str__(self):
        return f"Giỏ hàng của {self.customer.name}"
    
    def get_total(self):
        """Calculate total price of all items in cart"""
        total = sum(item.get_subtotal() for item in self.items.all())
        return total
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return self.items.aggregate(models.Sum('quantity'))['quantity__sum'] or 0
    
    def clear(self):
        """Remove all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """CartItem model representing an item in a cart"""
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Giỏ hàng'
    )
    book = models.ForeignKey(
        'store.Book',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Sách'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày thêm')
    
    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'book']
        verbose_name = 'Sản phẩm trong giỏ'
        verbose_name_plural = 'Sản phẩm trong giỏ'
    
    def __str__(self):
        return f"{self.quantity}x {self.book.title}"
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.book.price * self.quantity
