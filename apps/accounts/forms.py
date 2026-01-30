from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'nama', 'role', 'nisn', 'kelas', 'ampu_mapel', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'nisn': forms.TextInput(attrs={'class': 'form-control'}),
            'kelas': forms.Select(attrs={'class': 'form-select'}),
            'ampu_mapel': forms.SelectMultiple(attrs={'class': 'form-select select2', 'data-toggle': 'select2'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m() # Important for ampu_mapel
        return user
