from django.db import models


class StaffSchedule(models.Model):
    """Lịch làm việc nhân viên"""
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    SHIFT_TYPES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('full', 'Full Day'),
    ]
    
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'staff_schedules'
        unique_together = ['staff', 'day_of_week', 'shift_type']

    def __str__(self):
        return f"{self.staff.name} - {self.get_day_of_week_display()} ({self.get_shift_type_display()})"

    def get_hours(self):
        from datetime import datetime, timedelta
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        if end < start:
            end += timedelta(days=1)
        return (end - start).seconds / 3600
