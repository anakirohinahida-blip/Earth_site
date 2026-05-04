import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Earth.settings')
django.setup()

from django.contrib.auth.models import User

username = "admin"
email = "admin@example.com"
password = "admin123"

if not User.objects.filter(username=username).exists():
    print("Создаю суперпользователя...")
    User.objects.create_superuser(username, email, password)
else:
    print("Суперпользователь уже существует")