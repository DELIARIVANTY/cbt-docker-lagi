
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SHOW COLUMNS FROM exams_banksoal")
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns NOW:", columns)
    
    if 'mapel_id' in columns:
        print("SUCCESS: mapel_id exists.")
    else:
        print("FAILURE: mapel_id is missing.")
