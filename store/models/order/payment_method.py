from django.db import models


class PaymentMethod(models.Model):
    """Phương thức thanh toán"""
    PAYMENT_TYPES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cod', 'Cash on Delivery'),
        ('wallet', 'Digital Wallet'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES)
    description = models.TextField(blank=True)
    icon_url = models.CharField(max_length=500, blank=True)
    processing_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fee_type = models.CharField(max_length=20, choices=[('fixed', 'Fixed'), ('percentage', 'Percentage')], default='fixed')
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'payment_method_options'
        ordering = ['display_order']

    def __str__(self):
        return self.name

    def calculate_fee(self, amount):
        if self.fee_type == 'percentage':
            return amount * (self.processing_fee / 100)
        return self.processing_fee

    def is_available_for(self, amount):
        if amount < self.min_amount:
            return False
        if self.max_amount and amount > self.max_amount:
            return False
        return self.is_active
