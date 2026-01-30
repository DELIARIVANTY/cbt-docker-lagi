
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.academic.models import Kelas, Jurusan, MataPelajaran

def run_seed():
    print("Seeding Real Data (Username = Nama)...")

    # 1. Jurusan
    jurusan, created = Jurusan.objects.get_or_create(kode='PHASE_E', defaults={'nama': 'Fase E (Kurikulum Merdeka)'})
    
    # 2. Kelas X.E 7
    kelas, created = Kelas.objects.get_or_create(nama='X.E 7', jurusan=jurusan)
    print(f"Target Kelas: {kelas}")

    # 3. Guru (Wali Kelas) - Aa Herdiana, S.Pd
    guru_username = 'aa.herdiana'
    guru, created = CustomUser.objects.get_or_create(username=guru_username, defaults={
        'first_name': 'Aa Herdiana, S.Pd',
        'email': 'aa.herdiana@sekolah.id',
        'role': 'guru'
    })
    if created:
        guru.set_password('guru123')
        guru.save()
        print(f"Created Guru: {guru.username}")
    else:
        print(f"Using Guru: {guru.username}")

    # 4. Siswa Data
    students = [
        ("0101572286", "252610217", "AHMAD IHYA ULUMUDIN"),
        ("252610218", "252610218", "AKIB SYAPUTRA"),
        ("0091811980", "252610219", "ANBAR WIDIA PATAH"),
        ("0103105728", "252610220", "ANDRIAN DWI ADITYA"),
        ("0116712884", "252610221", "AYIPAH"),
        ("0093129968", "252610222", "CAHAYA BINTANG VIOLA"),
        ("0091021878", "252610223", "DESTRI"),
        ("0106756397", "252610224", "DINDA ZULFA AZAHRA"),
        ("0109689242", "252610225", "ELINA SELPIANA"),
        ("0109449047", "252610226", "FITRI ANISA"),
        ("252610227", "252610227", "IBNU AZIS HIDAYAT"),
        ("0107085496", "252610228", "ISTAYA SARI"),
        ("0096376339", "252610229", "JULEHA"),
        ("0107395548", "252610230", "KEVIN PAMUNGKAS"),
        ("0091021260", "252610231", "M. NURAMIN"),
        ("0102521713", "252610232", "MARYATI ULPAH"),
        ("0085470203", "252610233", "MUHAMAD ALI ISROK SAPUTRA"),
        ("0107557023", "252610234", "MUHAMAD BAYU"),
        ("006473859", "252610235", "MUHAMAD UCU"),
        ("0084994952", "252610236", "MUHAMMAD NURFIKRI"),
        ("0101808186", "252610237", "NADIL ARDIANSYAH"),
        ("0108605041", "252610238", "NASHWA ALMAIDA SUHADI"),
        ("0106975609", "252610239", "NUR AYUNI"),
        ("0101693148", "252610240", "PUTRI RAHAYU"),
        ("0096569665", "252610241", "RATNA SYIFA RAHMAN"),
        ("0101715764", "252610242", "RIDHO SETIAWAN"),
        ("0094149262", "252610243", "ROHAYATI"),
        ("0101259936", "252610244", "SAEKHUL IHSAN"),
        ("0104418013", "252610245", "SANDI SAPUTRA"),
        ("0096511090", "252610246", "SARTANA"),
        ("0105139038", "252610247", "SATIA DIKA"),
        ("010642234", "252610248", "SHIFA SAHFITRI"),
        ("0098260936", "252610249", "SITI MAHMUDAH"),
        ("0097344741", "252610250", "SUPIYATI"),
        ("0099151707", "252610251", "TIARA ANGINI"),
        ("0095005657", "252610262", "WAHYUDI"),
        ("0106726351", "252610253", "YOLA YULINDA"),
    ]

    # CLEANUP: Remove old student accounts in this class to replace with new usernames
    print(f"Deleting existing students in {kelas.nama}...")
    deleted_count, _ = CustomUser.objects.filter(kelas=kelas, role='siswa').delete()
    print(f"Deleted {deleted_count} old student accounts.")

    count = 0
    for nisn, nis, nama in students:
        # Generate Username: "ahmad.ihya.ulumudin"
        base_username = slugify(nama).replace('-', '.')
        username = base_username
        
        # Ensure uniqueness
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}.{counter}"
            counter += 1

        password = nisn if nisn else nis # Pass remains NISN
        
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=nama,
            role='siswa',
            kelas=kelas
        )
        count += 1
        print(f"Created: {username} (Pass: {password}) - {nama}")

    print(f"Done! Created {count} students with name-based usernames.")

if __name__ == '__main__':
    run_seed()
