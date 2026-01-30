from django.urls import path
from . import views, views_api

urlpatterns = [
    path('api/add-mapel/', views_api.api_add_mapel, name='api_add_mapel'),
    
    # Mapel CRUD
    path('mapel/', views.mapel_list, name='mapel_list'),
    path('mapel/create/', views.mapel_create, name='mapel_create'),
    path('mapel/<int:pk>/edit/', views.mapel_edit, name='mapel_edit'),
    path('mapel/<int:pk>/delete/', views.mapel_delete, name='mapel_delete'),
    
    # Kelas CRUD
    path('kelas/', views.kelas_list, name='kelas_list'),
    path('kelas/create/', views.kelas_create, name='kelas_create'),
    path('kelas/<int:pk>/edit/', views.kelas_edit, name='kelas_edit'),
    path('kelas/<int:pk>/delete/', views.kelas_delete, name='kelas_delete'),
    path('kelas/<int:pk>/kartu-peserta/', views.cetak_kartu_kelas, name='cetak_kartu_kelas'),
    
    # Jurusan CRUD
    path('jurusan/', views.jurusan_list, name='jurusan_list'),
    path('jurusan/create/', views.jurusan_create, name='jurusan_create'),
    path('jurusan/<int:pk>/edit/', views.jurusan_edit, name='jurusan_edit'),
    path('jurusan/<int:pk>/delete/', views.jurusan_delete, name='jurusan_delete'),
]
