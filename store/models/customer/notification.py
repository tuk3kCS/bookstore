from django.db import models


class Notification(models.Model):
    """Thông báo cho khách hàng"""
    NOTIFICATION_TYPES = [
        ('order', 'Order Update'),
        ('promotion', 'Promotion'),
        ('system', 'System'),
        ('reminder', 'Reminder'),
        ('wishlist', 'Wishlist'),
    ]
    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer} - {self.title}"

    def mark_as_read(self):
        self.is_read = True
        self.save()

    @classmethod
    def get_unread_count(cls, customer):
        return cls.objects.filter(customer=customer, is_read=False).count()
