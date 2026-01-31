from django.db import models


class StaffRole(models.Model):
    """Vai trò nhân viên"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'staff_roles'

    def __str__(self):
        return self.name

    def get_permissions(self):
        return self.permissions.filter(is_granted=True)

    def has_permission(self, permission_code):
        return self.permissions.filter(permission__code=permission_code, is_granted=True).exists()
