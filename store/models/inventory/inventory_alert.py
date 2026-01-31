from django.db import models


class InventoryAlert(models.Model):
    """Cảnh báo tồn kho"""
    ALERT_TYPES = [
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('overstock', 'Overstock'),
        ('expiring', 'Expiring Soon'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]
    
    book = models.ForeignKey('store.Book', on_delete=models.CASCADE, related_name='inventory_alerts')
    warehouse = models.ForeignKey('store.Warehouse', on_delete=models.CASCADE, null=True, blank=True)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_quantity = models.IntegerField()
    threshold = models.IntegerField()
    message = models.TextField()
    acknowledged_by = models.ForeignKey('store.Staff', on_delete=models.SET_NULL, null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_alert_type_display()}: {self.book.title}"

    def acknowledge(self, staff):
        from django.utils import timezone
        self.status = 'acknowledged'
        self.acknowledged_by = staff
        self.acknowledged_at = timezone.now()
        self.save()

    def resolve(self):
        self.status = 'resolved'
        self.save()

    @classmethod
    def check_low_stock(cls, book, threshold=10):
        from store.models.inventory.inventory import Inventory
        inv = Inventory.objects.filter(book=book).first()
        if inv and inv.quantity <= threshold:
            cls.objects.get_or_create(
                book=book,
                alert_type='low_stock',
                status='active',
                defaults={
                    'current_quantity': inv.quantity,
                    'threshold': threshold,
                    'message': f"Low stock alert: {book.title} has only {inv.quantity} units"
                }
            )
