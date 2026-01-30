
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SHOW COLUMNS FROM exams_banksoal")
    columns = [row[0] for row in cursor.fetchall()]
    
    if 'updated_at' not in columns:
        print("Adding 'updated_at' column...")
        # Try simple add with default
        try:
            cursor.execute("ALTER TABLE exams_banksoal ADD COLUMN updated_at datetime NULL")
            cursor.execute("UPDATE exams_banksoal SET updated_at = created_at")
            cursor.execute("ALTER TABLE exams_banksoal MODIFY COLUMN updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP")
            print("Successfully added updated_at.")
        except Exception as e:
            print(f"Error adding updated_at: {e}")
    else:
        print("'updated_at' already exists.")
