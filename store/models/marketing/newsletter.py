from django.db import models


class Newsletter(models.Model):
    """Bản tin email"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled'),
    ]
    
    subject = models.CharField(max_length=255)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    total_recipients = models.IntegerField(default=0)
    total_opened = models.IntegerField(default=0)
    total_clicked = models.IntegerField(default=0)
    created_by = models.ForeignKey('store.Staff', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'newsletters'

    def __str__(self):
        return self.subject

    def get_open_rate(self):
        if self.total_recipients == 0:
            return 0
        return (self.total_opened / self.total_recipients) * 100

    def get_click_rate(self):
        if self.total_recipients == 0:
            return 0
        return (self.total_clicked / self.total_recipients) * 100


class NewsletterSubscriber(models.Model):
    """Người đăng ký nhận bản tin"""
    email = models.EmailField(unique=True)
    customer = models.ForeignKey('store.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'newsletter_subscribers'

    def __str__(self):
        return self.email

    def unsubscribe(self):
        from django.utils import timezone
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()
