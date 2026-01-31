from django.db import models


class Tax(models.Model):
    """Thuế"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'taxes'
        verbose_name_plural = 'Taxes'

    def __str__(self):
        return self.name

    def get_rate_for_region(self, region):
        rate = self.rates.filter(region=region, is_active=True).first()
        return rate.rate if rate else 0


class TaxRate(models.Model):
    """Thuế suất theo vùng"""
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='rates')
    region = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    rate = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    is_compound = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tax_rates'
        unique_together = ['tax', 'region', 'country_code']

    def __str__(self):
        return f"{self.tax.name} - {self.region}: {self.rate}%"

    def calculate_tax(self, amount):
        return amount * (self.rate / 100)
