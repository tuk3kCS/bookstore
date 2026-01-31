"""
Staff Model - Staff Domain
Represents a staff member in the bookstore system
"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Staff(models.Model):
    """Staff model representing an employee"""
    
    name = models.CharField(max_length=100, verbose_name='Họ tên')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=128, verbose_name='Mật khẩu')
    staff_role = models.ForeignKey(
        'store.StaffRole',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members',
        verbose_name='Vai trò'
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Số điện thoại')
    hire_date = models.DateField(null=True, blank=True, verbose_name='Ngày vào làm')
    department = models.CharField(max_length=100, blank=True, verbose_name='Phòng ban')
    avatar = models.CharField(max_length=500, blank=True, verbose_name='Avatar URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    class Meta:
        db_table = 'staff'
        ordering = ['-created_at']
        verbose_name = 'Nhân viên'
        verbose_name_plural = 'Nhân viên'
    
    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"
    
    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password matches"""
        return check_password(raw_password, self.password)
    
    def is_admin(self):
        """Check if staff member is admin"""
        return self.staff_role and self.staff_role.code == 'admin'
    
    def has_permission(self, permission_code):
        """Check if staff has specific permission"""
        if not self.staff_role:
            return False
        return self.staff_role.has_permission(permission_code)
