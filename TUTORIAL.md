# Panduan Super Simpel: Menjalankan Project di GitHub Codespaces

Jika Anda bingung, bayangkan ini seperti **meminjam komputer canggih milik GitHub** untuk menjalankan aplikasi Anda, jadi Anda tidak perlu instal apa-apa di komputer sendiri (selain upload code).

## Konsep Dasar (Analogi)
*   **Laragon (Sekarang)**: Anda masak di **dapur rumah sendiri**. Semua alat (PHP, MySQL, Python) harus Anda beli dan pasang sendiri di laptop.
*   **GitHub Codespaces**: Anda menyewa **dapur profesional siap pakai** di cloud (internet). Semua alat (Python, Database) sudah disiapkan otomatis oleh file yang saya buat tadi (`Dockerfile`).

---

## Langkah 1: Upload ke GitHub (Wajib)
Komputer GitHub tidak bisa membaca file di laptop Anda. Jadi, file-file ini harus ada di GitHub dulu.

1.  Buka terminal di folder project ini.
2.  Ketik perintah ini satu per satu (tekan Enter setiap baris):
    ```bash
    git init
    git add .
    git commit -m "Siap untuk Codespaces"
    ```
    *Catatan: Jika muncul error "fatal: not a git repository", itu karena Anda belum menjalankan `git init`. Perintah pertama di atas sudah mengatasinya.*

3.  Sekarang Anda perlu membuat repository baru di GitHub.com:
    - Buka [GitHub.com/new](https://github.com/new).
    - Beri nama repository, misalnya `bisaplis-cbt`.
    - Klik **Create repository**.
    - Salin perintah yang muncul di bagian **"…or push an existing repository from the command line"**.
    - Tempel (paste) perintah itu di terminal Anda dan tekan Enter.


## Langkah 2: Nyalakan Codespaces
1.  Buka browser (Chrome/Edge), masuk ke halaman repository GitHub Anda.
2.  Cari tombol warna hijau bertuliskan **<> Code**.
3.  Klik tab **Codespaces**.
4.  Klik tombol hijau **Create codespace on main**.
5.  Akan muncul tab baru dengan tampilan mirip VS Code. **Tunggu saja** (bisa 2-5 menit) sampai proses loading selesai. Jangan ditutup.

## Langkah 3: Jalankan Aplikasi
Saat tampilan Codespaces sudah siap (mirip VS Code biasa):
1.  Lihat ada **Terminal** di bagian bawah.
2.  Ketik perintah ini untuk menyiapkan database (karena ini komputer baru, databasenya masih kosong):
    ```bash
    python manage.py migrate
    ```
3.  Nyalakan servernya:
    ```bash
    python manage.py runserver
    ```
4.  Akan muncul notifikasi kecil di pojok kanan bawah: *"Your application is running on port 8000"*. Klik tombol **Open in Browser**.

**Selesai!** Website Anda sekarang berjalan di internet (Codespaces), bukan di Laragon.

---

## Pertanyaan Sering Muncul

**Q: Apakah data di Laragon saya hilang?**
A: Tidak. Data di Laragon aman di laptop Anda. Data di Codespaces terpisah.

**Q: Kalau saya edit kode di Codespaces, apakah file di laptop berubah?**
A: Tidak otomatis. Anda harus melakukan `git push` di Codespaces, lalu `git pull` di laptop jika ingin menyamakan.

**Q: Apakah ini bayar?**
A: GitHub memberikan jatah gratis 60 jam per bulan untuk pengguna akun gratis (Free). Ini cukup untuk belajar/coba-coba.
