from django.db import models


class ReturnOrder(models.Model):
    """Đơn trả hàng"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('received', 'Received'),
        ('refunded', 'Refunded'),
    ]
    
    REASON_CHOICES = [
        ('damaged', 'Damaged Product'),
        ('wrong_item', 'Wrong Item'),
        ('not_as_described', 'Not As Described'),
        ('changed_mind', 'Changed Mind'),
        ('other', 'Other'),
    ]
    
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='returns')
    customer = models.ForeignKey('store.Customer', on_delete=models.CASCADE, related_name='returns')
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    reason_detail = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'return_orders'

    def __str__(self):
        return f"Return #{self.id} for Order #{self.order.id}"

    def approve(self):
        self.status = 'approved'
        self.save()

    def reject(self, notes=''):
        self.status = 'rejected'
        self.admin_notes = notes
        self.save()

    def calculate_refund(self):
        return sum(item.get_refund_amount() for item in self.items.all())


class ReturnOrderItem(models.Model):
    """Chi tiết đơn trả hàng"""
    return_order = models.ForeignKey(ReturnOrder, on_delete=models.CASCADE, related_name='items')
    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    condition = models.CharField(max_length=50, choices=[
        ('new', 'New/Unopened'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ])

    class Meta:
        db_table = 'return_order_items'

    def __str__(self):
        return f"{self.quantity}x {self.order_item.book.title}"

    def get_refund_amount(self):
        return self.order_item.price * self.quantity
