from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from leaves import views as leave_views # Make sure this import is correct

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Add the "Empty Path" for your main dashboard
    path('', leave_views.teacher_dashboard, name='teacher_dashboard'),

    # 2. Add the Admin Panel path
    path('admin-panel/', leave_views.admin_dashboard, name='admin_dashboard'),

    # 3. Your existing Login/Logout paths
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]