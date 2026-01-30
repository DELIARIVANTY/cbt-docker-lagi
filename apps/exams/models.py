from django.db import models
from django.conf import settings
from apps.academic.models import MataPelajaran, Kelas

class BankSoal(models.Model):
    judul = models.CharField(max_length=200)
    kode = models.CharField(max_length=20, unique=True, blank=True)
    mapel = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    guru = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'guru'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.kode:
            import random, string
            self.kode = "BNK-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

class ButirSoal(models.Model):
    JENIS_CHOICES = (
        ('PG', 'Pilihan Ganda'),
        ('ESSAY', 'Essay / Uraian'),
    )
    bank_soal = models.ForeignKey(BankSoal, on_delete=models.CASCADE, related_name='questions')
    jenis_soal = models.CharField(max_length=10, choices=JENIS_CHOICES, default='PG')
    pertanyaan = models.TextField()
    gambar = models.ImageField(upload_to='soal_images/', blank=True, null=True)
    audio = models.FileField(upload_to='soal_audio/', blank=True, null=True)
    opsi_a = models.TextField(blank=True, null=True)
    opsi_b = models.TextField(blank=True, null=True)
    opsi_c = models.TextField(blank=True, null=True)
    opsi_d = models.TextField(blank=True, null=True)
    opsi_e = models.TextField(blank=True, null=True)
    
    KUNCI_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    )
    # Kunci jawaban can be nullable for Essay, or store text for Essay simple matching (but usually Teacher grades manual)
    kunci_jawaban = models.CharField(max_length=1, choices=KUNCI_CHOICES, blank=True, null=True)
    bobot = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.bank_soal.judul} - {self.id} ({self.jenis_soal})"

class Ujian(models.Model):
    bank_soal = models.ForeignKey(BankSoal, on_delete=models.CASCADE)
    nama_ujian = models.CharField(max_length=200)
    kelas = models.ManyToManyField(Kelas)
    waktu_mulai = models.DateTimeField()
    durasi = models.IntegerField(help_text="Durasi dalam menit")
    token = models.CharField(max_length=6, blank=True)
    SEMESTER_CHOICES = (
        ('Ganjil', 'Ganjil'),
        ('Genap', 'Genap'),
    )
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='Ganjil')
    aktif = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.token:
            import random, string
            self.token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_ujian

class SesiUjian(models.Model):
    STATUS_CHOICES = (
        ('ONGOING', 'Mengerjakan'),
        ('WAITING_GRADE', 'Menunggu Koreksi'),
        ('GRADED', 'Selesai Dinilai'),
    )
    ujian = models.ForeignKey(Ujian, on_delete=models.CASCADE)
    siswa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'siswa'})
    waktu_mulai = models.DateTimeField(auto_now_add=True)
    waktu_selesai = models.DateTimeField(null=True, blank=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ONGOING')
    nilai = models.FloatField(default=0.0)
    score = models.FloatField(default=0.0) # Raw Score (DB Sync)
    sisa_waktu = models.IntegerField(default=0) # Seconds remaining
    
    def __str__(self):
        return f"{self.siswa.username} - {self.ujian.nama_ujian}"

class JawabanSiswa(models.Model):
    sesi = models.ForeignKey(SesiUjian, on_delete=models.CASCADE, related_name='jawaban_siswa', db_column='sesi_ujian_id')
    soal = models.ForeignKey(ButirSoal, on_delete=models.CASCADE, db_column='butir_soal_id')
    jawaban = models.CharField(max_length=1, blank=True, null=True, db_column='jawaban_dipilih') # A, B, C, D, E
    jawaban_essay = models.TextField(blank=True, null=True) # For Essay
    score = models.FloatField(default=0.0) # Score per item (auto for PG, manual for Essay)
    ragu_ragu = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sesi', 'soal')

    def __str__(self):
        return f"{self.sesi} - {self.soal.id}"

class JadwalPengawas(models.Model):
    ujian = models.ForeignKey(Ujian, on_delete=models.CASCADE, related_name='jadwal_pengawas')
    kelas = models.ForeignKey('academic.Kelas', on_delete=models.CASCADE)
    proktor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'guru'})

    class Meta:
        unique_together = ('ujian', 'kelas') # Satu kelas dalam satu ujian hanya punya 1 pengawas

    def __str__(self):
        return f"{self.proktor.username} - {self.ujian.nama_ujian} ({self.kelas.nama})"
