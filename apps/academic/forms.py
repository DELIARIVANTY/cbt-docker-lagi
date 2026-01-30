from django import forms
from .models import MataPelajaran, Kelas, Jurusan

class MataPelajaranForm(forms.ModelForm):
    class Meta:
        model = MataPelajaran
        fields = ['kode', 'nama']
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
        }

class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = ['nama', 'jurusan', 'tingkat']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: X IPA 1'}),
            'jurusan': forms.Select(attrs={'class': 'form-select'}),
            'tingkat': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class JurusanForm(forms.ModelForm):
    class Meta:
        model = Jurusan
        fields = ['kode', 'nama']
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
        }
