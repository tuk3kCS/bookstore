from django.db import models


class ShippingMethod(models.Model):
    """Phương thức vận chuyển"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_days_min = models.IntegerField(default=1)
    estimated_days_max = models.IntegerField(default=7)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'shipping_method_options'

    def __str__(self):
        return self.name

    def calculate_cost(self, weight=0):
        return self.base_cost + (self.cost_per_kg * weight)

    def get_estimated_delivery(self):
        if self.estimated_days_min == self.estimated_days_max:
            return f"{self.estimated_days_min} days"
        return f"{self.estimated_days_min}-{self.estimated_days_max} days"
