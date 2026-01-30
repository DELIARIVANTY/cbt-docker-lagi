
import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

from apps.accounts.models import CustomUser as User
from apps.academic.models import Kelas, MataPelajaran, Jurusan
from apps.exams.models import BankSoal, ButirSoal, Ujian

def create_test_data():
    print("Creating test data...")

    # 1. Create/Get Master Data
    jurusan, _ = Jurusan.objects.get_or_create(nama="IPA", kode="IPA")
    
    kelas_nama = "XII IPA 1 (Test)"
    # Note: tingkat=12 based on the name XII
    kelas, _ = Kelas.objects.get_or_create(nama=kelas_nama, jurusan=jurusan, defaults={'tingkat': 12})
    print(f"Class: {kelas.nama}")

    # 2. Create Users
    # Teacher
    guru, _ = User.objects.get_or_create(
        username="guru_test",
        email="guru@test.com",
        defaults={'role': 'guru', 'nama': 'Pak Guru Test'}
    )
    if _:
        guru.set_password('123456')
        guru.save()
    print(f"Teacher: {guru.username}")

    # Student
    siswa, _ = User.objects.get_or_create(
        username="siswa_test",
        email="siswa@test.com",
        defaults={'role': 'siswa', 'nama': 'Budi Siswa Test', 'kelas': kelas}
    )
    if _:
        siswa.set_password('123456')
        siswa.save()
    else:
        # Ensure student is in the class
        siswa.kelas = kelas
        siswa.save()
    print(f"Student: {siswa.username} / 123456")

    # 3. Create Subject
    mapel, _ = MataPelajaran.objects.get_or_create(nama="Matematika Dasar", kode="MAT-DAS")
    
    # 4. Create Bank Soal
    bank, _ = BankSoal.objects.get_or_create(
        judul="Latihan Ujian Matematika",
        mapel=mapel,
        guru=guru,
        defaults={'kode': 'BANK-TEST-001'}
    )
    
    # 5. Create Questions (if empty)
    if bank.questions.count() == 0:
        print("Creating questions...")
        # Create 5 PG questions
        for i in range(1, 6):
            ButirSoal.objects.create(
                bank_soal=bank,
                jenis_soal='PG',
                pertanyaan=f"Pertanyaan Nomor {i}: Berapakah {i} + {i}?",
                opsi_a=str(i+i), # Correct
                opsi_b=str(i+i+1),
                opsi_c=str(i+i+2),
                opsi_d=str(i+i+3),
                opsi_e=str(i+i+4),
                kunci_jawaban='A',
                bobot=10
            )
        # Create 1 Essay
        ButirSoal.objects.create(
            bank_soal=bank,
            jenis_soal='ESSAY',
            pertanyaan="Jelaskan kenapa 1+1=2?",
            bobot=50
        )
    
    # 6. Create Active Exam
    ujian, created = Ujian.objects.get_or_create(
        nama_ujian="Ujian Percobaan Sistem",
        bank_soal=bank,
        defaults={
            'waktu_mulai': timezone.now() - timedelta(minutes=10), # Started 10 mins ago
            'durasi': 120, # 2 hours
            'token': 'TEST01',
            'semester': 'Ganjil',
            'aktif': True
        }
    )
    if not created:
        # Update to ensure it's active and valid
        ujian.waktu_mulai = timezone.now() - timedelta(minutes=10)
        ujian.aktif = True
        ujian.token = 'TEST01'
        ujian.save()
    
    ujian.kelas.add(kelas)
    
    print("-" * 30)
    print("DATA GENERATED SUCCESSFULLY")
    print("-" * 30)
    print(f"Login Siswa  : {siswa.username}")
    print(f"Password     : 123456")
    print(f"Token Ujian  : {ujian.token}")
    print(f"Nama Ujian   : {ujian.nama_ujian}")
    print("-" * 30)

if __name__ == '__main__':
    create_test_data()
