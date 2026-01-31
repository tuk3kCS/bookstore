from django.db import models


class AuditLog(models.Model):
    """Nhật ký hệ thống - ghi lại các hoạt động"""
    ACTION_TYPES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('export', 'Export'),
        ('import', 'Import'),
    ]
    
    user_type = models.CharField(max_length=20, choices=[('staff', 'Staff'), ('customer', 'Customer'), ('system', 'System')])
    user_id = models.IntegerField(null=True, blank=True)
    user_name = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    object_repr = models.CharField(max_length=255, blank=True)
    changes = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} {self.action} {self.model_name}"

    @classmethod
    def log(cls, user_type, user_id, user_name, action, model_name, object_id=None, object_repr='', changes=None, request=None):
        ip_address = None
        user_agent = ''
        if request:
            ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        return cls.objects.create(
            user_type=user_type,
            user_id=user_id,
            user_name=user_name,
            action=action,
            model_name=model_name,
            object_id=object_id,
            object_repr=object_repr,
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent
        )
