from django.db import models


class ShippingZone(models.Model):
    """Vùng vận chuyển"""
    name = models.CharField(max_length=100)
    countries = models.TextField(help_text="Comma-separated country codes")
    regions = models.TextField(blank=True, help_text="Comma-separated region names")
    shipping_methods = models.ManyToManyField('ShippingMethod', through='ShippingZoneRate')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'shipping_zones'

    def __str__(self):
        return self.name

    def get_countries_list(self):
        return [c.strip() for c in self.countries.split(',')]

    def is_available_for(self, country_code):
        return country_code.upper() in self.get_countries_list()


class ShippingZoneRate(models.Model):
    """Tỷ lệ vận chuyển theo vùng"""
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE)
    shipping_method = models.ForeignKey('ShippingMethod', on_delete=models.CASCADE)
    rate_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'shipping_zone_rates'
        unique_together = ['zone', 'shipping_method']

    def calculate_rate(self, base_cost):
        return (base_cost * self.rate_multiplier) + self.additional_cost
