
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SHOW COLUMNS FROM exams_banksoal")
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns BEFORE:", columns)
    
    if 'mata_pelajaran_id' in columns and 'mapel_id' not in columns:
        print("Renaming 'mata_pelajaran_id' to 'mapel_id'...")
        cursor.execute("ALTER TABLE exams_banksoal CHANGE mata_pelajaran_id mapel_id bigint(20) NOT NULL")
        print("Rename successful.")
    
    # Check for updated_at
    if 'updated_at' not in columns:
        print("Adding 'updated_at' column...")
        cursor.execute("ALTER TABLE exams_banksoal ADD COLUMN updated_at datetime(6) NOT NULL DEFAULT NOW()")
    
    cursor.execute("SHOW COLUMNS FROM exams_banksoal")
    print("Columns AFTER:", [row[0] for row in cursor.fetchall()])
