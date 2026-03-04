from django.contrib import admin
from .models import Student, LeaveRecord # <--- MUST BE HERE TOO

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_phone', 'teacher')
    list_filter = ('teacher',) # Admin can filter students by Teacher
    search_fields = ('name',)

@admin.register(LeaveRecord)
class LeaveRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'timestamp', 'reason')
    list_filter = ('timestamp', 'student') # This creates your history filters
    readonly_fields = ('timestamp',) # Keeps the history accurate

    # Helper to show which teacher marked the leave in the history list
    def get_teacher(self, obj):
        return obj.student.teacher
    get_teacher.short_description = 'Teacher'


