from django.db import models
from django.utils import timezone


class Banner(models.Model):
    """Banner quảng cáo"""
    POSITIONS = [
        ('home_hero', 'Home Hero'),
        ('home_sidebar', 'Home Sidebar'),
        ('category_top', 'Category Top'),
        ('product_sidebar', 'Product Sidebar'),
        ('footer', 'Footer'),
    ]
    
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True)
    image_url = models.CharField(max_length=500)
    image_alt = models.CharField(max_length=255, blank=True)
    link_url = models.CharField(max_length=500, blank=True)
    position = models.CharField(max_length=50, choices=POSITIONS)
    display_order = models.IntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    click_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'banners'
        ordering = ['position', 'display_order']

    def __str__(self):
        return f"{self.title} ({self.get_position_display()})"

    def is_visible(self):
        if not self.is_active:
            return False
        now = timezone.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True

    def record_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def record_click(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])

    def get_ctr(self):
        """Click-through rate"""
        if self.view_count == 0:
            return 0
        return (self.click_count / self.view_count) * 100
