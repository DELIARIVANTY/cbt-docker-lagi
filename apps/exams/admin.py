from django.contrib import admin
from .models import BankSoal, ButirSoal, Ujian, SesiUjian, JawabanSiswa

class ButirSoalInline(admin.TabularInline):
    model = ButirSoal
    extra = 1

@admin.register(BankSoal)
class BankSoalAdmin(admin.ModelAdmin):
    list_display = ('judul', 'mapel', 'guru', 'created_at')
    list_filter = ('mapel', 'guru')
    inlines = [ButirSoalInline]

@admin.register(Ujian)
class UjianAdmin(admin.ModelAdmin):
    list_display = ('nama_ujian', 'bank_soal', 'waktu_mulai', 'durasi', 'token', 'aktif')
    list_filter = ('aktif', 'waktu_mulai')
    filter_horizontal = ('kelas',)

@admin.register(SesiUjian)
class SesiUjianAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'ujian', 'waktu_mulai', 'waktu_selesai', 'is_finished')
    list_filter = ('is_finished', 'ujian')

@admin.register(JawabanSiswa)
class JawabanSiswaAdmin(admin.ModelAdmin):
    list_display = ('sesi', 'soal', 'jawaban', 'ragu_ragu')
    list_filter = ('ragu_ragu',)
