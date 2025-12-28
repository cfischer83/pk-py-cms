from django import forms
from .models import Media


class MediaUploadForm(forms.ModelForm):
    """Form for uploading media files."""
    
    class Meta:
        model = Media
        fields = ['file', 'title', 'alt_text', 'caption']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*,video/*,audio/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter title (optional, will use filename)',
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Alternative text for images',
            }),
            'caption': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Enter caption (optional)',
            }),
        }
