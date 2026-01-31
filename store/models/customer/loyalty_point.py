from django.db import models


class LoyaltyPoint(models.Model):
    """Điểm thưởng của khách hàng"""
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='loyalty')
    total_points = models.IntegerField(default=0)
    available_points = models.IntegerField(default=0)
    lifetime_points = models.IntegerField(default=0)
    tier = models.CharField(max_length=50, default='Bronze')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'loyalty_points'

    def __str__(self):
        return f"{self.customer} - {self.available_points} points"

    def add_points(self, points):
        self.total_points += points
        self.available_points += points
        self.lifetime_points += points
        self.update_tier()
        self.save()

    def redeem_points(self, points):
        if points <= self.available_points:
            self.available_points -= points
            self.save()
            return True
        return False

    def update_tier(self):
        if self.lifetime_points >= 10000:
            self.tier = 'Platinum'
        elif self.lifetime_points >= 5000:
            self.tier = 'Gold'
        elif self.lifetime_points >= 1000:
            self.tier = 'Silver'
        else:
            self.tier = 'Bronze'
