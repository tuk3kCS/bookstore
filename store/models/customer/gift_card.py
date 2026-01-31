from django.db import models
from django.utils import timezone
import secrets


class GiftCard(models.Model):
    """Thẻ quà tặng"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('disabled', 'Disabled'),
    ]
    
    code = models.CharField(max_length=20, unique=True)
    initial_value = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    purchaser = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, related_name='purchased_gift_cards')
    recipient = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='received_gift_cards')
    recipient_email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gift_cards'

    def __str__(self):
        return f"Gift Card {self.code} - ${self.current_balance}"

    @classmethod
    def generate_code(cls):
        return secrets.token_hex(8).upper()

    def is_valid(self):
        return self.status == 'active' and self.expiry_date >= timezone.now().date() and self.current_balance > 0

    def use(self, amount):
        if amount <= self.current_balance:
            self.current_balance -= amount
            if self.current_balance == 0:
                self.status = 'used'
            self.save()
            return True
        return False
