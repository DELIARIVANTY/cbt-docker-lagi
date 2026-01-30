import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_system.settings')
django.setup()

from apps.accounts.models import CustomUser as User
from apps.academic.models import Kelas, Jurusan

def create_username_from_name(nama):
    """
    Convert full name to username format (firstname.lastname)
    Example: "Heri Sumarya, S.Pd." -> "heri.sumarya"
    """
    # Remove titles and degrees
    nama = re.sub(r',?\s*S\.\w+\.?', '', nama)  # Remove S.Pd, S.Ag, S.H, etc
    nama = re.sub(r',?\s*\w+\.', '', nama)  # Remove other titles
    
    # Clean up
    nama = nama.strip().replace(',', '')
    
    # Split and get first and last name
    parts = nama.split()
    if len(parts) >= 2:
        firstname = parts[0].lower()
        lastname = parts[-1].lower()
        username = f"{firstname}.{lastname}"
    else:
        # If only one word, use it twice
        username = f"{parts[0].lower()}.{parts[0].lower()}"
    
    # Remove special characters
    username = re.sub(r'[^a-z.]', '', username)
    
    return username

def seed_data():
    print("=" * 50)
    print("SEEDING DATA GURU DAN KELAS")
    print("=" * 50)
    
    # 1. Buat Jurusan
    print("\n[1] Membuat Jurusan...")
    jurusan_e, _ = Jurusan.objects.get_or_create(nama="E", kode="E")
    jurusan_f, _ = Jurusan.objects.get_or_create(nama="F", kode="F")
    print(f"   ✓ Jurusan E: {jurusan_e}")
    print(f"   ✓ Jurusan F: {jurusan_f}")
    
    # 2. Hapus guru lama yang menggunakan format guru01, guru02, etc
    print("\n[2] Membersihkan data guru lama...")
    deleted_count = User.objects.filter(username__startswith='guru', role='guru').delete()[0]
    print(f"   ✓ {deleted_count} guru lama dihapus")
    
    # 3. Buat Data Guru
    print("\n[3] Membuat Data Guru dengan username baru...")
    data_guru = [
        "Heri Sumarya, S.Pd.",
        "M. Hamdani, S.Pd.I",
        "Dadang Robi Suheri",
        "Sumaji, S.Pd.",
        "Andi, S.Pd.",
        "Didi Gunelis, S.Pd.",
        "Musnalini",
        "Abdul Muhkaram H, S.Pd.",
        "Marlina",
        "Jajang A",
        "Abdul Mulya, S.Pd.",
        "Heri Nur Jaro, S.Pd.",
        "E. Rambe Donikus Halim, S.Pd.",
        "Mulyana, S.Pd.",
        "Suherlan, S.Pd.I",
        "Endra Gunawan",
        "Yusuf Ismail, S.Ag.",
        "Irfan Dwi Ardiansyah, S.Pd.I",
        "Irine Ramdini, S.Pd.",
        "Dida wani Ratih, S.Pd.",
        "Siti Marhanah Marina, S.Pd.",
        "Rida Sri Candra Wahyurini, S.H.",
        "Lucky Ramdhana",
        "Nasrun, S.Pd.",
        "Suhaider, S.Pd.",
        "Edi Suhelis, S.Pd.",
        "Syarif, S.Pd.I",
        "Irul Sobrul, S.Pd.",
        "Risti Azdiatuni, S.Pd.",
        "Slapy Ramdian Susy, S.Pd.",
        "M Mahmat Nasrip, S.Pd.",
        "Firmany, S",
        "Ihsan Muharam, S.Pd.I",
        "Didi Gunella, S.Pd.",
        "Nengshi Handini Salsab",
    ]
    
    guru_created = 0
    guru_skipped = 0
    
    for nama in data_guru:
        username = create_username_from_name(nama)
        
        # Check if username already exists, if so add number
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'nama': nama,
                'role': 'guru',
                'email': f'{username}@smk.sch.id'
            }
        )
        if created:
            user.set_password('guru123')
            user.save()
            guru_created += 1
            print(f"   ✓ {username:25s} | {nama}")
        else:
            guru_skipped += 1
            print(f"   - {username:25s} | {nama} (sudah ada)")
    
    print(f"\n   Guru dibuat: {guru_created}, Dilewati: {guru_skipped}")
    
    # 4. Buat Data Kelas (jika belum ada)
    print("\n[4] Membuat Data Kelas...")
    
    kelas_e = ["E1", "E2", "E3", "E4", "E5", "E6"]
    kelas_f = ["F1", "F2", "F3", "F4", "F5", "F6"]
    
    kelas_created = 0
    
    for nama_kelas in kelas_e:
        kelas, created = Kelas.objects.get_or_create(
            nama=nama_kelas,
            jurusan=jurusan_e,
            defaults={'tingkat': 10}
        )
        if created:
            kelas_created += 1
            print(f"   ✓ Kelas {nama_kelas} (Jurusan E)")
        else:
            print(f"   - Kelas {nama_kelas} (sudah ada)")
    
    for nama_kelas in kelas_f:
        kelas, created = Kelas.objects.get_or_create(
            nama=nama_kelas,
            jurusan=jurusan_f,
            defaults={'tingkat': 10}
        )
        if created:
            kelas_created += 1
            print(f"   ✓ Kelas {nama_kelas} (Jurusan F)")
        else:
            print(f"   - Kelas {nama_kelas} (sudah ada)")
    
    print(f"\n   Kelas dibuat: {kelas_created}, Dilewati: {len(kelas_e) + len(kelas_f) - kelas_created}")
    
    # 5. Summary
    print("\n" + "=" * 50)
    print("SEEDING SELESAI!")
    print("=" * 50)
    print(f"Total Jurusan : {Jurusan.objects.count()}")
    print(f"Total Guru    : {User.objects.filter(role='guru').count()}")
    print(f"Total Kelas   : {Kelas.objects.count()}")
    print("\nPassword default semua guru: guru123")
    print("\nContoh username guru:")
    for user in User.objects.filter(role='guru')[:5]:
        print(f"  - {user.username} ({user.nama})")
    print("=" * 50)

if __name__ == '__main__':
    seed_data()
