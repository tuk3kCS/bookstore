from django.db import models


class PurchaseOrder(models.Model):
    """Đơn nhập hàng từ nhà cung cấp"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='purchase_orders')
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='purchase_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    expected_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey('store.Staff', on_delete=models.SET_NULL, null=True, related_name='created_purchase_orders')
    approved_by = models.ForeignKey('store.Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_purchase_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchase_orders'

    def __str__(self):
        return f"PO-{self.id:05d}"

    def calculate_total(self):
        self.total_amount = sum(item.get_subtotal() for item in self.items.all())
        self.save()
        return self.total_amount

    def get_grand_total(self):
        return self.total_amount + self.tax_amount + self.shipping_cost

    def approve(self, staff):
        self.status = 'approved'
        self.approved_by = staff
        self.save()

    def receive(self):
        from django.utils import timezone
        self.status = 'received'
        self.received_date = timezone.now().date()
        self.save()
        # Create stock movements for each item
        for item in self.items.all():
            StockMovement.objects.create(
                book=item.book,
                warehouse=self.warehouse,
                movement_type='in',
                quantity=item.quantity,
                reference=str(self),
                created_by=self.created_by
            )


class PurchaseOrderItem(models.Model):
    """Chi tiết đơn nhập hàng"""
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('store.Book', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    received_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'purchase_order_items'

    def __str__(self):
        return f"{self.quantity}x {self.book.title}"

    def get_subtotal(self):
        return self.quantity * self.unit_price
