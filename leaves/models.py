from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    # This links the student to a specific teacher
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})

    def __str__(self):
        return self.name

class LeaveRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True) # Automatic history date/time
    reason = models.CharField(max_length=255, default="Absent")

    def __str__(self):
        return f"{self.student.name} - {self.timestamp.strftime('%Y-%m-%d')}"