import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

def fix_schema():
    with connection.cursor() as cursor:
        print("Fixing exams_butirsoal schema...")
        
        # 1. Drop 'jenis_soal' if exists (so migration can add it cleanly)
        try:
            cursor.execute("ALTER TABLE exams_butirsoal DROP COLUMN jenis_soal;")
            print("Dropped jenis_soal.")
        except Exception as e:
            print(f"jenis_soal drop failed (maybe didn't exist): {e}")

        # 2. Drop 'options' and 'teks_bacaan' (garbage from other version)
        try:
            cursor.execute("ALTER TABLE exams_butirsoal DROP COLUMN options;")
            print("Dropped options.")
        except Exception as e:
            print(f"options drop failed: {e}")
            
        try:
            cursor.execute("ALTER TABLE exams_butirsoal DROP COLUMN teks_bacaan;")
            print("Dropped teks_bacaan.")
        except Exception as e:
            print(f"teks_bacaan drop failed: {e}")

        # 3. Add 'opsi_a' ... 'opsi_e' if missing
        for col in ['opsi_a', 'opsi_b', 'opsi_c', 'opsi_d', 'opsi_e']:
            try:
                # Check if exists first? Or just try ADD and ignore error?
                # MySQL won't add if exists usually throws error.
                # Let's try to add. Assuming TEXT type (based on models.py)
                cursor.execute(f"ALTER TABLE exams_butirsoal ADD COLUMN {col} LONGTEXT;")
                print(f"Added {col}.")
            except Exception as e:
                print(f"Add {col} failed (likely exists): {e}")

    print("Schema fix complete.")

if __name__ == '__main__':
    fix_schema()
