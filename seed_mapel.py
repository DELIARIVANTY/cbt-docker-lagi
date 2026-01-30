
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

from apps.academic.models import MataPelajaran

subjects = [
    ('Pendidikan Agama dan Budi Pekerti', 'PABP'),
    ('Pendidikan Pancasila dan Kewarganegaraan', 'PPKN'),
    ('Bahasa Indonesia', 'BIN'),
    ('Matematika (Wajib)', 'MAT-W'),
    ('Matematika (Peminatan)', 'MAT-P'),
    ('Sejarah Indonesia', 'SEJ-IND'),
    ('Bahasa Inggris', 'BING'),
    ('Seni Budaya', 'SENBUD'),
    ('Pendidikan Jasmani, Olahraga, dan Kesehatan', 'PJOK'),
    ('Prakarya dan Kewirausahaan', 'PKWU'),
    ('Biologi', 'BIO'),
    ('Fisika', 'FIS'),
    ('Kimia', 'KIM'),
    ('Geografi', 'GEO'),
    ('Sejarah (Peminatan)', 'SEJ-PEM'),
    ('Sosiologi', 'SOS'),
    ('Ekonomi', 'EKO'),
    ('Informatika', 'INF'),
    ('Bahasa Arab', 'BARAB'),
    ('Bahasa Mandarin', 'BMAND'),
]

print("Seeding Mata Pelajaran...")
created_count = 0
for nama, kode in subjects:
    obj, created = MataPelajaran.objects.get_or_create(
        kode=kode,
        defaults={'nama': nama}
    )
    if created:
        print(f"[CREATED] {nama} ({kode})")
        created_count += 1
    else:
        print(f"[EXISTS] {nama} ({kode})")

print(f"\nDone. Added {created_count} new subjects.")
