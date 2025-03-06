from django import forms
from .models import StatusMessage

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['text']

    # Remove ClearableFileInput, just use FileField and let the HTML input handle the 'multiple' attribute
    files = forms.FileField(required=False)
