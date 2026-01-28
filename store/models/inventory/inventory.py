"""
Inventory Model - Inventory Domain
Represents inventory transactions (import/export) in the bookstore system
"""
from django.db import models


class Inventory(models.Model):
    """Inventory model representing stock transactions"""
    
    TRANSACTION_TYPE_CHOICES = [
        ('import', 'Nhập kho'),
        ('export', 'Xuất kho'),
        ('return', 'Trả hàng'),
        ('adjustment', 'Điều chỉnh'),
    ]
    
    book = models.ForeignKey(
        'store.Book',
        on_delete=models.CASCADE,
        related_name='inventory_transactions',
        verbose_name='Sách'
    )
    supplier = models.ForeignKey(
        'store.Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_transactions',
        verbose_name='Nhà cung cấp'
    )
    staff = models.ForeignKey(
        'store.Staff',
        on_delete=models.SET_NULL,
        null=True,
        related_name='inventory_transactions',
        verbose_name='Nhân viên thực hiện'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='Loại giao dịch'
    )
    quantity = models.IntegerField(verbose_name='Số lượng')
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Đơn giá'
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Tổng tiền'
    )
    note = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    reference_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Số tham chiếu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    
    class Meta:
        db_table = 'inventory'
        ordering = ['-created_at']
        verbose_name = 'Giao dịch kho'
        verbose_name_plural = 'Giao dịch kho'
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.book.title} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Override save to calculate total and update stock"""
        self.total_amount = self.quantity * self.unit_price
        
        # Update book stock
        if self.pk is None:  # Only on create
            if self.transaction_type == 'import':
                self.book.stock_quantity += self.quantity
            elif self.transaction_type in ['export', 'adjustment']:
                self.book.stock_quantity -= self.quantity
            elif self.transaction_type == 'return':
                self.book.stock_quantity += self.quantity
            self.book.save()
        
        super().save(*args, **kwargs)
