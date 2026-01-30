# 4.5.3. Hak Akses

Implementasi hak akses dalam Sistem CBT ini menerapkan prinsip *Least Privilege*, di mana setiap pengguna hanya diberikan akses sesuai dengan kebutuhan tugas dan fungsinya. Hak akses dikelompokkan menjadi dua kategori utama:

### a. Petugas yang Berwenang

Petugas yang berwenang adalah pengguna yang terlibat langsung dalam operasional teknis, manajemen data, dan pelaksanaan kegiatan evaluasi sehari-hari.

1.  **Administrator (Superuser)**
    *   **Wewenang**: Memiliki akses penuh (root access) terhadap seluruh fitur dan data dalam sistem.
    *   **Tanggung Jawab**:
        *   Manajemen data master (User, Mata Pelajaran, Kelas, Jurusan).
        *   Maintenance sistem dan database.
        *   Konfigurasi jadwal global.
        *   Penyelesaian kendala teknis tingkat sistem.

2.  **Guru Mata Pelajaran**
    *   **Wewenang**: Terbatas pada pengelolaan konten akademik sesuai mata pelajaran yang diampu.
    *   **Tanggung Jawab**:
        *   Pembuatan dan pengelolaan Bank Soal (Input soal, import soal).
        *   Penyusunan jadwal ujian untuk kelas yang diajar.
        *   Proses koreksi jawaban (terutama soal Essay).
        *   Evaluasi hasil ujian per mata pelajaran.

3.  **Proktor / Panitia Ujian**
    *   **Wewenang**: Fokus pada pengawasan dan kelancaran teknis saat ujian berlangsung.
    *   **Tanggung Jawab**:
        *   Monitoring status peserta ujian secara real-time.
        *   Mereset login peserta yang mengalami gangguan teknis.
        *   Memastikan integritas pelaksanaan ujian (mencegah kecurangan).
        *   Mencetak berita acara dan daftar hadir ujian.

### b. Pimpinan

Pimpinan adalah pengguna yang memiliki hak akses untuk memantau kinerja sistem dan hasil evaluasi secara manajerial tanpa terlibat dalam operasional teknis harian.

1.  **Waka Kurikulum / Kepala Sekolah**
    *   **Wewenang**: Akses *Read-Only* (hanya melihat) terhadap data laporan dan statistik, serta monitoring kegiatan.
    *   **Tanggung Jawab**:
        *   Monitoring statistik pelaksanaan ujian secara global.
        *   Melihat rekapitulasi nilai siswa per semester, jurusan, atau kelas.
        *   Mengevaluasi kinerja guru dalam pembuatan soal dan pelaksanaan ujian.
        *   Mengambil keputusan berbasis data hasil analisis ujian (misal: analisis tingkat kesukaran soal).
    *   **Batasan**: Tidak dapat mengubah data inti (soal, nilai, user) untuk menjaga validitas data laporan.
