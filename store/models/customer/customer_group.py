from django.db import models


class CustomerGroup(models.Model):
    """Nhóm khách hàng - VIP, Regular, New, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    points_multiplier = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customer_groups'

    def __str__(self):
        return self.name

    def get_member_count(self):
        return self.customers.count()

    def apply_discount(self, amount):
        return amount * (1 - self.discount_percentage / 100)
