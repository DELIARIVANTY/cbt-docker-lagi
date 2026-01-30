from django.urls import path
from . import views

urlpatterns = [
    path('bank-soal/', views.bank_soal_list, name='bank_soal_list'),
    path('bank-soal/create/', views.bank_soal_create, name='bank_soal_create'),
    path('bank-soal/<int:pk>/', views.bank_soal_detail, name='bank_soal_detail'),
    path('bank-soal/<int:pk>/import/', views.import_soal, name='import_soal'),
    path('bank-soal/download-template/', views.download_template, name='download_template'),
    path('bank-soal/<int:pk>/import/commit/', views.import_commit, name='import_commit'),
    path('bank-soal/<int:pk>/add-manual/', views.butir_soal_create, name='butir_soal_create'),
    path('bank-soal/<int:pk>/edit/', views.bank_soal_edit, name='bank_soal_edit'),
    path('butir-soal/<int:pk>/edit/', views.butir_soal_edit, name='butir_soal_edit'),
    path('butir-soal/<int:pk>/delete/', views.butir_soal_delete, name='butir_soal_delete'),
    path('bank-soal/<int:pk>/delete/', views.bank_soal_delete, name='bank_soal_delete'),
    
    # Ujian URLs
    path('ujian/', views.ujian_list, name='ujian_list'),
    path('ujian/create/', views.ujian_create, name='ujian_create'),
    path('ujian/<int:pk>/edit/', views.ujian_edit, name='ujian_edit'),
    path('ujian/<int:pk>/delete/', views.ujian_delete, name='ujian_delete'),
    path('ujian/<int:pk>/hasil/', views.hasil_ujian, name='hasil_ujian'),
    path('koreksi/', views.koreksi_list, name='koreksi_list'),
    path('koreksi/<int:pk>/', views.koreksi_detail, name='koreksi_detail'),
    
    # Student Exam Flow
    path('ujian/<int:pk>/konfirmasi/', views.konfirmasi_ujian, name='konfirmasi_ujian'),
    path('ujian/<int:pk>/mulai/', views.mulai_ujian, name='mulai_ujian'),
    path('ujian/simpan-jawaban/', views.simpan_jawaban, name='simpan_jawaban'),
    path('ujian/<int:pk>/selesai/', views.selesai_ujian, name='selesai_ujian'),
    path('ujian/<int:pk>/analisis/', views.analisis_ujian, name='analisis_ujian'),
    path('ujian/<int:pk>/analisis/export/', views.analisis_export, name='analisis_export'),
    path('ujian/<int:pk>/analisis/export-pdf/', views.analisis_export_pdf, name='analisis_export_pdf'),
    path('ujian/<int:pk>/export-nilai/', views.export_nilai_siswa, name='export_nilai_siswa'),
    path('ujian/<int:pk>/export-nilai-pdf/', views.export_nilai_siswa_pdf, name='export_nilai_siswa_pdf'),
    path('ujian/<int:pk>/analisis/chart/', views.chart_analisis, name='chart_analisis'),
    
    # Phase 6: Extra Features
    path('bank-soal/<int:pk>/export/', views.export_bank_soal, name='export_bank_soal'),
    path('ujian/<int:pk>/regenerate-token/', views.regenerate_token, name='regenerate_token'),
    path('ujian/<int:pk>/monitoring/', views.monitoring_ujian, name='monitoring_ujian'),
    path('sesi/<int:pk>/force-finish/', views.force_finish_exam, name='force_finish_exam'),
    path('sesi/<int:pk>/reset-login/', views.reset_login, name='reset_login'),
    path('sesi/<int:pk>/cetak/', views.cetak_kartu_ujian, name='cetak_kartu_ujian'),
    path('ujian/<int:pk>/kartu-peserta/', views.kartu_peserta_ujian, name='kartu_peserta_ujian'),
    path('ujian/<int:pk>/atur-pengawas/', views.atur_pengawas, name='atur_pengawas'),
    
    # Jadwal Pengawas CRUD (Global Management)
    path('pengawas/', views.jadwal_pengawas_list, name='jadwal_pengawas_list'),
    path('pengawas/create/', views.jadwal_pengawas_create, name='jadwal_pengawas_create'),
    path('pengawas/<int:pk>/edit/', views.jadwal_pengawas_edit, name='jadwal_pengawas_edit'),
    path('pengawas/<int:pk>/delete/', views.jadwal_pengawas_delete, name='jadwal_pengawas_delete'),
]
