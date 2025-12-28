from django import forms
from .models import User


class LoginForm(forms.Form):
    """Form for user login."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        })
    )


class RegisterForm(forms.ModelForm):
    """Form for user registration."""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm password',
        })
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email address',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'First name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Last name',
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')
        
        return cleaned_data


class ProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'avatar', 'website']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://example.com',
            }),
        }
