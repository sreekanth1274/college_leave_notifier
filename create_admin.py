import os
import django
from django.contrib.auth import get_user_model

# Ensure this matches your folder name 'school_notifier'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_notifier.settings')
django.setup()

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    print("Superuser created successfully!")