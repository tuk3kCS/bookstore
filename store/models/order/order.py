"""
Order and OrderItem Models - Order Domain
Represents order functionality
"""
from django.db import models


class Order(models.Model):
    """Order model representing a customer order"""
    
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
    ]
    
    customer = models.ForeignKey(
        'store.Customer',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Khách hàng'
    )
    shipping = models.ForeignKey(
        'store.Shipping',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='Phương thức giao hàng'
    )
    payment = models.ForeignKey(
        'store.Payment',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='Phương thức thanh toán'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Tổng tiền'
    )
    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Phí giao hàng'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Trạng thái'
    )
    shipping_address = models.TextField(verbose_name='Địa chỉ giao hàng')
    shipping_phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    note = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đặt hàng')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
    
    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.customer.name}"
    
    def get_subtotal(self):
        """Get subtotal (before shipping)"""
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_grand_total(self):
        """Get grand total (including shipping)"""
        return self.get_subtotal() + self.shipping_fee
    
    def calculate_total(self):
        """Calculate and update total price"""
        subtotal = self.get_subtotal()
        self.total_price = subtotal + self.shipping_fee
        self.save()


class OrderItem(models.Model):
    """OrderItem model representing an item in an order"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Đơn hàng'
    )
    book = models.ForeignKey(
        'store.Book',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Sách'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Giá tại thời điểm mua'
    )
    
    class Meta:
        db_table = 'order_items'
        verbose_name = 'Sản phẩm trong đơn hàng'
        verbose_name_plural = 'Sản phẩm trong đơn hàng'
    
    def __str__(self):
        return f"{self.quantity}x {self.book.title}"
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.price * self.quantity
