from .models import SheetMusic
from django import forms

class SheetMusicForm(forms.ModelForm):
    class Meta:
        model = SheetMusic
        fields = ['title', 'composer', 'difficulty', 'category', 'pdf_file', 'cover_image']

    def clean_pdf_file(self):
        file = self.cleaned_data.get('pdf_file')

        if file:
            if not file.name.endswith(('.pdf', '.mscz')):
                raise forms.ValidationError('Only PDF or MSCZ files are allowed.')
        return file