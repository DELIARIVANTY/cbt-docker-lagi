from django import forms

class ImportSoalForm(forms.Form):
    file = forms.FileField(label='File Excel (.xlsx)', help_text='Format: Pertanyaan, Opsi A, Opsi B, Opsi C, Opsi D, Opsi E, Kunci, Bobot')
