from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from .models import Benutzer


class RegistrierungsForm(UserCreationForm):
    """Formular für die Benutzerregistrierung"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ihre@email.de',
            'class': 'form-input'
        })
    )

    class Meta:
        model = Benutzer
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Max Mustermann',
                'class': 'form-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': '••••••••',
            'class': 'form-input'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '••••••••',
            'class': 'form-input'
        })


class LoginForm(AuthenticationForm):
    """Formular für den Login"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Benutzername',
            'class': 'form-input'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': '••••••••',
            'class': 'form-input'
        })
