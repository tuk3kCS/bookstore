"""
Coupon Model - Order Domain
Represents discount coupons in the bookstore system
"""
from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    """Coupon model for discount codes"""
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Phần trăm'),
        ('fixed', 'Số tiền cố định'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name='Mã giảm giá')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage',
        verbose_name='Loại giảm giá'
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Giá trị giảm')
    min_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Giá trị đơn hàng tối thiểu'
    )
    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Giảm tối đa'
    )
    usage_limit = models.PositiveIntegerField(blank=True, null=True, verbose_name='Số lần sử dụng tối đa')
    used_count = models.PositiveIntegerField(default=0, verbose_name='Số lần đã sử dụng')
    start_date = models.DateTimeField(verbose_name='Ngày bắt đầu')
    end_date = models.DateTimeField(verbose_name='Ngày kết thúc')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'coupons'
        ordering = ['-created_at']
        verbose_name = 'Mã giảm giá'
        verbose_name_plural = 'Mã giảm giá'
    
    def __str__(self):
        return f"{self.code} - {self.get_discount_display()}"
    
    def get_discount_display(self):
        """Get formatted discount display"""
        if self.discount_type == 'percentage':
            return f"{self.discount_value}%"
        return f"{self.discount_value:,.0f}đ"
    
    def is_valid(self):
        """Check if coupon is still valid"""
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.start_date or now > self.end_date:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        return True
    
    def calculate_discount(self, order_total):
        """Calculate discount amount for given order total"""
        if order_total < self.min_purchase:
            return 0
        
        if self.discount_type == 'percentage':
            discount = order_total * (self.discount_value / 100)
        else:
            discount = self.discount_value
        
        if self.max_discount and discount > self.max_discount:
            discount = self.max_discount
        
        return min(discount, order_total)
    
    def use(self):
        """Increment used count"""
        self.used_count += 1
        self.save()
