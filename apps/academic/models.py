from django.db import models

class Jurusan(models.Model):
    nama = models.CharField(max_length=50)  # e.g. IPA, IPS, TKJ
    kode = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nama

class Kelas(models.Model):
    nama = models.CharField(max_length=50) # e.g. X IPA 1
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)
    tingkat = models.IntegerField(default=10, help_text="10, 11, 12")
    
    def __str__(self):
        return self.nama

class MataPelajaran(models.Model):
    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.nama
