from django.core.management.base import BaseCommand
from apps.academic.models import Jurusan, Kelas, MataPelajaran

class Command(BaseCommand):
    help = 'Populates database with standard SMA data (Jurusan, Kelas, Mapel)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating SMA Data...')

        # 1. Jurusan
        jurusans = [('IPA', 'IPA'), ('IPS', 'IPS'), ('Bahasa', 'BHS')]
        jurusan_objs = {}
        for nama, kode in jurusans:
            obj, created = Jurusan.objects.get_or_create(nama=nama, defaults={'kode': kode})
            jurusan_objs[nama] = obj
            if created:
                self.stdout.write(f'Created Jurusan: {nama}')

        # 2. Kelas
        tingkats = ['X', 'XI', 'XII']
        for tingkat in tingkats:
            for nama_jurusan, jurusan_obj in jurusan_objs.items():
                # Create 3 classes for each level/major (e.g., X IPA 1, X IPA 2, X IPA 3)
                for i in range(1, 4):
                    nama_kelas = f"{tingkat} {nama_jurusan} {i}"
                    kelas_obj, created = Kelas.objects.get_or_create(
                        nama=nama_kelas,
                        jurusan=jurusan_obj
                    )
                    if created:
                        self.stdout.write(f'Created Kelas: {nama_kelas}')

        # 3. Mata Pelajaran
        mapels = [
            ('Matematika Wajib', 'MAT-W'), ('Matematika Peminatan', 'MAT-P'),
            ('Fisika', 'FIS'), ('Kimia', 'KIM'), ('Biologi', 'BIO'),
            ('Ekonomi', 'EKO'), ('Sosiologi', 'SOS'), ('Geografi', 'GEO'),
            ('Bahasa Indonesia', 'BIN'), ('Bahasa Inggris', 'BIG'),
            ('Pendidikan Kewarganegaraan', 'PKN'), ('Sejarah Indonesia', 'SEJ-I'), ('Sejarah Peminatan', 'SEJ-P'),
            ('Pendidikan Agama Islam', 'PAI'), ('Pendidikan Jasmani', 'PJOK'), ('Seni Budaya', 'SBY'),
            ('Prakarya dan Kewirausahaan', 'PKWU')
        ]
        
        for nama, kode in mapels:
            obj, created = MataPelajaran.objects.get_or_create(nama=nama, defaults={'kode': kode})
            if created:
                self.stdout.write(f'Created Mapel: {nama}')

        self.stdout.write(self.style.SUCCESS('Successfully populated SMA data'))
