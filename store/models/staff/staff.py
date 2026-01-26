"""
Staff Model - Staff Domain
Represents a staff member in the bookstore system
"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Staff(models.Model):
    """Staff model representing an employee"""
    
    ROLE_CHOICES = [
        ('admin', 'Quản trị viên'),
        ('staff', 'Nhân viên'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Họ tên')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=128, verbose_name='Mật khẩu')
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff',
        verbose_name='Vai trò'
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Số điện thoại')
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
        return self.role == 'admin'
