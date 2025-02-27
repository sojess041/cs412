from django import forms
from .models import StatusMessage

class CreateStatusMessageForm(forms.ModelForm):
    """
    Form to create a new StatusMessage.
    """
    class Meta:
        model = StatusMessage
        fields = ['message'] 
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a Message', 'class': 'form-control'})
        }