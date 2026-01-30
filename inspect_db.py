import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

def check_columns():
    with connection.cursor() as cursor:
        print("Checking ButirSoal columns:")
        cursor.execute("DESCRIBE exams_butirsoal;")
        for row in cursor.fetchall():
            print(row[0])
            
        print("\nChecking JawabanSiswa columns:")
        cursor.execute("DESCRIBE exams_jawabansiswa;")
        for row in cursor.fetchall():
            print(row[0])

        print("\nChecking SesiUjian columns:")
        cursor.execute("DESCRIBE exams_sesiujian;")
        for row in cursor.fetchall():
            print(row[0])

if __name__ == '__main__':
    check_columns()
