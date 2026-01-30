from django import forms
from .models import BankSoal, ButirSoal, Ujian

class BankSoalForm(forms.ModelForm):
    class Meta:
        model = BankSoal
        fields = ['judul', 'mapel']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control'}),
            'mapel': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'guru':
            self.fields['mapel'].queryset = user.ampu_mapel.all()

class ButirSoalForm(forms.ModelForm):
    class Meta:
        model = ButirSoal
        fields = ['pertanyaan', 'gambar', 'audio', 'jenis_soal', 'opsi_a', 'opsi_b', 'opsi_c', 'opsi_d', 'opsi_e', 'kunci_jawaban', 'bobot']
        widgets = {
            'pertanyaan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gambar': forms.FileInput(attrs={'class': 'form-control'}),
            'audio': forms.FileInput(attrs={'class': 'form-control'}),
            'jenis_soal': forms.Select(attrs={'class': 'form-select'}),
            'opsi_a': forms.TextInput(attrs={'class': 'form-control'}),
            'opsi_b': forms.TextInput(attrs={'class': 'form-control'}),
            'opsi_c': forms.TextInput(attrs={'class': 'form-control'}),
            'opsi_d': forms.TextInput(attrs={'class': 'form-control'}),
            'opsi_e': forms.TextInput(attrs={'class': 'form-control'}),
            'kunci_jawaban': forms.Select(attrs={'class': 'form-select'}),
            'bobot': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UjianForm(forms.ModelForm):
    class Meta:
        model = Ujian
        fields = ['nama_ujian', 'bank_soal', 'kelas', 'semester', 'waktu_mulai', 'durasi', 'token', 'aktif']
        widgets = {
            'nama_ujian': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_soal': forms.Select(attrs={'class': 'form-select'}),
            'kelas': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'waktu_mulai': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'durasi': forms.NumberInput(attrs={'class': 'form-control'}),
            'token': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kosongkan untuk auto-generate'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['token'].required = False

from .models import JadwalPengawas
from apps.accounts.models import CustomUser
from apps.academic.models import Kelas

class JadwalPengawasForm(forms.ModelForm):
    class Meta:
        model = JadwalPengawas
        fields = ['ujian', 'kelas', 'proktor']
        widgets = {
            'ujian': forms.Select(attrs={'class': 'form-select'}),
            'kelas': forms.Select(attrs={'class': 'form-select'}),
            'proktor': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'proktor': 'Pengawas (Guru)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show teachers (guru) in proktor dropdown
        self.fields['proktor'].queryset = CustomUser.objects.filter(role='guru').order_by('nama')
        self.fields['proktor'].label_from_instance = lambda obj: f"{obj.nama} ({obj.username})"
