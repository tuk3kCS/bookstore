from django.db import models
from django.utils import timezone


class BookDiscount(models.Model):
    """Giảm giá cho sách cụ thể"""
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='discounts')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book_discounts'

    def __str__(self):
        return f"{self.book.title} - {self.discount_value}{'%' if self.discount_type == 'percentage' else '$'}"

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def calculate_discounted_price(self, original_price):
        if not self.is_valid():
            return original_price
        if self.discount_type == 'percentage':
            return original_price * (1 - self.discount_value / 100)
        return max(0, original_price - self.discount_value)
