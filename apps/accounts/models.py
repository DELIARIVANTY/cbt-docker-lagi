from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        # Ensure plain_password is set before saving
        extra_fields['plain_password'] = password
        return super()._create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    objects = CustomUserManager()

    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('guru', 'Guru'),
        ('siswa', 'Siswa'),
        ('proktor', 'Proktor/Panitia'),
        ('waka', 'Waka Kurikulum'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='siswa')
    nama = models.CharField(max_length=255, verbose_name="Nama Lengkap", default="")
    nisn = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name="NISN (Siswa)")
    kelas = models.ForeignKey('academic.Kelas', on_delete=models.SET_NULL, null=True, blank=True, related_name='siswa_set')
    ampu_mapel = models.ManyToManyField('academic.MataPelajaran', blank=True, related_name='guru_set', help_text="Mata pelajaran yang diampu (khusus Guru)")

    plain_password = models.CharField(max_length=128, blank=True, null=True, help_text="Password in plain text (generated automatically)")

    def set_password(self, raw_password):
        self.plain_password = raw_password
        super().set_password(raw_password)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
