from django.contrib import admin
from .models import Jurusan, Kelas, MataPelajaran

@admin.register(Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kode')
    search_fields = ('nama', 'kode')

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jurusan')
    list_filter = ('jurusan',)
    search_fields = ('nama',)

@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kode')
    search_fields = ('nama', 'kode')
