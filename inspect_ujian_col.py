
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SHOW COLUMNS FROM exams_ujian")
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns in exams_ujian:", columns)
    
    if 'aktif' not in columns:
        print("ALERT: 'aktif' column is MISSING!")
        # Attempt to add it? Better to let user know or do it via SQL
        # cursor.execute("ALTER TABLE exams_ujian ADD COLUMN aktif tinyint(1) NOT NULL DEFAULT 0")
        # print("Attempted to add 'aktif' column manually.")
    else:
        print("'aktif' column matches.")
