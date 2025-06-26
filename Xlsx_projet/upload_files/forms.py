
from django import forms
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Выберите файл Excel', validators=[FileExtensionValidator(allowed_extensions=['xlsx'])], widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx'
        })
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("Файл слишком большой (макс. 5MB)")
        return file
