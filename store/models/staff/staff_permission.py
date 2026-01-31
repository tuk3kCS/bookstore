from django.db import models


class StaffPermission(models.Model):
    """Quyền hạn"""
    PERMISSION_CATEGORIES = [
        ('book', 'Book Management'),
        ('order', 'Order Management'),
        ('customer', 'Customer Management'),
        ('inventory', 'Inventory Management'),
        ('staff', 'Staff Management'),
        ('report', 'Reports'),
        ('system', 'System Settings'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=PERMISSION_CATEGORIES)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'staff_permissions'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"


class RolePermission(models.Model):
    """Quyền hạn theo vai trò"""
    role = models.ForeignKey('StaffRole', on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(StaffPermission, on_delete=models.CASCADE)
    is_granted = models.BooleanField(default=True)

    class Meta:
        db_table = 'role_permissions'
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"
