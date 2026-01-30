
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SHOW COLUMNS FROM exams_ujian")
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns BEFORE:", columns)
    
    if 'is_active' in columns and 'aktif' not in columns:
        print("Renaming 'is_active' to 'aktif'...")
        cursor.execute("ALTER TABLE exams_ujian CHANGE is_active aktif tinyint(1) NOT NULL DEFAULT 0")
        print("Rename successful.")
    elif 'aktif' in columns:
        print("'aktif' column already exists.")
    else:
        print("Neither 'is_active' nor 'aktif' found. Check table structure.")
        
    cursor.execute("SHOW COLUMNS FROM exams_ujian")
    print("Columns AFTER:", [row[0] for row in cursor.fetchall()])
