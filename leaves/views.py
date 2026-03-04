from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from .models import Student, LeaveRecord
from .utils import send_leave_sms

# --- 1. Forms ---
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'parent_phone']

class TeacherCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

# --- 2. Admin Check ---
def is_admin(user):
    return user.is_superuser

from django.contrib.auth.decorators import user_passes_test

# This function checks if the user is a Superuser (Main Admin)
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Admin sees ALL students from ALL teachers
    all_students = Student.objects.all()
    all_teachers_count = User.objects.filter(is_staff=True).count()
    total_sms_sent = LeaveRecord.objects.count()

    return render(request, 'leaves/admin_dashboard.html', {
        'students': all_students,
        'teacher_count': all_teachers_count,
        'sms_count': total_sms_sent
    })
# --- 3. The Admin Dashboard (Principal View) ---
@login_required
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    if request.method == "POST":
        if 'add_teacher' in request.POST:
            form = TeacherCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.is_staff = True  # This makes them a "Teacher"
                user.is_superuser = False # Ensure they aren't an Admin
                user.save()
                messages.success(request, f"Teacher {user.username} added!")
                return redirect('admin_dashboard')

        elif 'delete_teacher' in request.POST:
            teacher_id = request.POST.get('teacher_id')
            User.objects.filter(id=teacher_id).delete()
            messages.warning(request, "Teacher account removed.")
            return redirect('admin_dashboard')

    # Fix: Fetch everyone who is staff but NOT the superuser (The Teachers)
    all_teachers = User.objects.filter(is_staff=True, is_superuser=False)
    
    selected_teacher_id = request.GET.get('teacher')
    selected_teacher = None
    students = []

    if selected_teacher_id:
        selected_teacher = get_object_or_404(User, id=selected_teacher_id)
        students = Student.objects.filter(teacher=selected_teacher)

    return render(request, 'leaves/admin_dashboard.html', {
        'teachers': all_teachers,
        'students': students,
        'selected_teacher': selected_teacher,
        'teacher_count': all_teachers.count(),
        'sms_count': LeaveRecord.objects.count(),
    })

# --- 4. The Teacher Dashboard (Class View) ---
@login_required
def teacher_dashboard(request):

    if request.user.is_superuser:
        return redirect('admin_dashboard')
    if request.method == "POST":
        # 1. Handle Bulk SMS
        if 'send_bulk_sms' in request.POST:
            student_ids = request.POST.getlist('selected_students') # Gets all checked IDs
            
            if not student_ids:
                # Optional: add a message saying "No students selected"
                return redirect('teacher_dashboard')

            for sid in student_ids:
                student = get_object_or_404(Student, id=sid)
                success = send_leave_sms(student.parent_phone, student.name)
                
                if success:
                    LeaveRecord.objects.create(student=student, reason="Absent")
            
            return redirect('teacher_dashboard')

        # 2. Handle Add Student (Same as before)
        elif 'add_student' in request.POST:
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.teacher = request.user
                student.save()
                return redirect('teacher_dashboard')

    my_students = Student.objects.filter(teacher=request.user)
    return render(request, 'leaves/dashboard.html', {'students': my_students})
    