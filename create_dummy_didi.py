import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.academic.models import MataPelajaran, Kelas, Jurusan
from apps.exams.models import BankSoal, Ujian, ButirSoal

User = get_user_model()

def create_dummy_data():
    # 1. Get or Create User didi.gunelis
    username = "didi.gunelis"
    email = "didi.gunelis@example.com"
    password = "password123"
    
    user, created = User.objects.get_or_create(username=username, defaults={
        'email': email,
        'role': 'guru',
        'nama': 'Didi Gunelis'
    })
    
    if created:
        user.set_password(password)
        user.save()
        print(f"Created user: {user.username}")
    else:
        print(f"User exists: {user.username}")

    # 2. Ensure Dependencies (Mapel, Kelas)
    # Jurusan
    jurusan, _ = Jurusan.objects.get_or_create(kode="MIPA", defaults={'nama': 'Matematika dan Ilmu Pengetahuan Alam'})
    
    # Mapel - Create a dummy one if none exists or specific one
    mapel, _ = MataPelajaran.objects.get_or_create(kode="MAT-XD", defaults={'nama': 'Matematika X Dummy'})
    
    # Kelas
    kelas, _ = Kelas.objects.get_or_create(nama="X MIPA 1", defaults={'jurusan': jurusan, 'tingkat': 10})

    # 3. Create 10 Bank Soal & Ujan
    print("Creating 10 Bank Soal and Ujian...")
    
    for i in range(1, 11):
        # Bank Soal
        judul_bank = f"Bank Soal Matematika {i} - Didi"
        bank_soal = BankSoal.objects.create(
            judul=judul_bank,
            mapel=mapel,
            guru=user
        )
        
        # Add some dummy questions to the bank (optional but good for completeness)
        for q in range(1, 6): # 5 questions per bank
            ButirSoal.objects.create(
                bank_soal=bank_soal,
                jenis_soal='PG',
                pertanyaan=f"Pertanyaan dummy nomor {q} untuk {judul_bank}?",
                opsi_a="Opsi A",
                opsi_b="Opsi B",
                opsi_c="Opsi C",
                opsi_d="Opsi D",
                opsi_e="Opsi E",
                kunci_jawaban=random.choice(['A', 'B', 'C', 'D', 'E']),
                bobot=1
            )

        # Ujian
        nama_ujian = f"Ujian Harian {i} - Didi"
        waktu_mulai = timezone.now() + timedelta(days=i)
        ujian = Ujian.objects.create(
            bank_soal=bank_soal,
            nama_ujian=nama_ujian,
            waktu_mulai=waktu_mulai,
            durasi=90,
            semester='Ganjil',
            aktif=True
        )
        ujian.kelas.add(kelas)
        
        print(f"Created: {bank_soal.judul} -> {ujian.nama_ujian}")

    print("Done! Successfully created 10 dummy data sets.")

if __name__ == '__main__':
    create_dummy_data()
