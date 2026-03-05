import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_notifier.settings')
django.setup()

User = get_user_model()
# Change 'admin', 'admin@example.com', and 'password123' to what you want
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")