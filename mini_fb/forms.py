from django import forms
from .models import StatusMessage
from .models import Profile

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['text']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'city', 'image_file']

class UpdateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['text'] 

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image_file', 'bio']
