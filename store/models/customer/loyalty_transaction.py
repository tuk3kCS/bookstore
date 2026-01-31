from django.db import models


class LoyaltyTransaction(models.Model):
    """Giao dịch điểm thưởng"""
    TRANSACTION_TYPES = [
        ('earn', 'Earn'),
        ('redeem', 'Redeem'),
        ('expire', 'Expire'),
        ('adjust', 'Adjustment'),
    ]
    
    loyalty = models.ForeignKey('LoyaltyPoint', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    description = models.CharField(max_length=255)
    order = models.ForeignKey('store.Order', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loyalty_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.loyalty.customer} - {self.transaction_type}: {self.points}"

    def get_points_display(self):
        prefix = '+' if self.transaction_type == 'earn' else '-'
        return f"{prefix}{abs(self.points)}"
