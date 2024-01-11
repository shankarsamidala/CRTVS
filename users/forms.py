# forms.py
from django import forms
from .models import VideoUpload

class VideoUpdateForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['subject_type', 'number_of_videos', 'remarks']
