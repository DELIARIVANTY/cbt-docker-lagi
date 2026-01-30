import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbt_system.settings")
django.setup()

from apps.accounts.models import CustomUser

username = "proktor1"
password = "password123"
email = "proktor1@school.id"

if CustomUser.objects.filter(username=username).exists():
    print(f"User {username} already exists.")
else:
    user = CustomUser.objects.create_user(username=username, email=email, password=password)
    user.role = 'proktor'
    user.save()
    print(f"Successfully created proktor: {username} / {password}")
