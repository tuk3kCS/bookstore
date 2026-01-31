from django.db import models


class Warehouse(models.Model):
    """Kho hàng"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    manager = models.ForeignKey('store.Staff', on_delete=models.SET_NULL, null=True, related_name='managed_warehouses')
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'warehouses'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_total_stock(self):
        return sum(s.quantity for s in self.stocks.all())

    def get_low_stock_items(self, threshold=10):
        return self.stocks.filter(quantity__lte=threshold)
