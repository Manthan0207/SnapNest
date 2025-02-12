from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['img_title', 'category', 'desc', 'image']  # These are the fields to show in the form
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter a detailed description of the pin.'}),
        }
