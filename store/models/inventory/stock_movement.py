from django.db import models


class StockMovement(models.Model):
    """Chuyển động kho - nhập/xuất/chuyển kho"""
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
    ]
    
    book = models.ForeignKey('store.Book', on_delete=models.CASCADE, related_name='stock_movements')
    warehouse = models.ForeignKey('store.Warehouse', on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=100, blank=True)  # PO number, Order number, etc.
    from_warehouse = models.ForeignKey('store.Warehouse', on_delete=models.SET_NULL, null=True, blank=True, related_name='outgoing_transfers')
    to_warehouse = models.ForeignKey('store.Warehouse', on_delete=models.SET_NULL, null=True, blank=True, related_name='incoming_transfers')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('store.Staff', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock_movements'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()}: {self.quantity} x {self.book.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update inventory after movement
        self.update_inventory()

    def update_inventory(self):
        from store.models.inventory.inventory import Inventory
        inv, created = Inventory.objects.get_or_create(
            book=self.book,
            defaults={'quantity': 0}
        )
        if self.movement_type in ['in', 'return']:
            inv.quantity += self.quantity
        elif self.movement_type == 'out':
            inv.quantity -= self.quantity
        inv.save()
