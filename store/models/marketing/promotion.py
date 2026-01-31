from django.db import models
from django.utils import timezone


class Promotion(models.Model):
    """Chương trình khuyến mãi"""
    PROMOTION_TYPES = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount'),
        ('buy_x_get_y', 'Buy X Get Y'),
        ('free_shipping', 'Free Shipping'),
    ]
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    applies_to_all = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'promotions'

    def __str__(self):
        return self.name

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.start_date or now > self.end_date:
            return False
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False
        return True

    def calculate_discount(self, amount):
        if not self.is_valid() or amount < self.min_purchase:
            return 0
        
        if self.promotion_type == 'percentage':
            discount = amount * (self.discount_value / 100)
        elif self.promotion_type == 'fixed':
            discount = self.discount_value
        else:
            discount = 0
            
        if self.max_discount:
            discount = min(discount, self.max_discount)
        return discount

    def use(self):
        self.usage_count += 1
        self.save()


class PromotionRule(models.Model):
    """Quy tắc khuyến mãi - áp dụng cho sản phẩm/danh mục cụ thể"""
    RULE_TYPES = [
        ('category', 'Category'),
        ('book', 'Specific Book'),
        ('author', 'Author'),
        ('publisher', 'Publisher'),
    ]
    
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='rules')
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    target_id = models.IntegerField()  # ID of category, book, author, or publisher

    class Meta:
        db_table = 'promotion_rules'

    def __str__(self):
        return f"{self.promotion.name} - {self.get_rule_type_display()}: {self.target_id}"
