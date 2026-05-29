from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    vorname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Max',
            'class': 'auth-input'
        }),
        label='Vorname'
    )
    nachname = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Mustermann',
            'class': 'auth-input'
        }),
        label='Nachname'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'deine@email.de',
            'class': 'auth-input'
        }),
        label='E-Mail'
    )
    passwort = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'auth-input'
        }),
        label='Passwort',
        help_text='Mindestens 8 Zeichen, 1 Großbuchstabe, 1 Zahl'
    )
    passwort_bestaetigen = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'auth-input'
        }),
        label='Passwort bestätigen'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Diese E-Mail-Adresse ist bereits registriert.')
        return email

    def clean_vorname(self):
        vorname = self.cleaned_data.get('vorname')
        if User.objects.filter(username=vorname.lower()).exists():
            raise ValidationError('Dieser Vorname ist bereits vergeben.')
        return vorname

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('passwort')
        pw2 = cleaned.get('passwort_bestaetigen')
        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError('Die Passwörter stimmen nicht überein.')
        return cleaned

    def save(self):
        vorname = self.cleaned_data['vorname']
        nachname = self.cleaned_data.get('nachname', '')
        email = self.cleaned_data['email']
        passwort = self.cleaned_data['passwort']
        # Username = Vorname (kleingeschrieben)
        user = User.objects.create_user(
            username=vorname.lower(),
            email=email,
            password=passwort,
            first_name=vorname,
            last_name=nachname
        )
        return user

def clean_neues_passwort(self):
    pw = self.cleaned_data.get('neues_passwort')
    if pw:
        if len(pw) < 8:
            raise forms.ValidationError('Mindestens 8 Zeichen.')
        if not any(c.isupper() for c in pw):
            raise forms.ValidationError('Mindestens 1 Großbuchstabe.')
        if not any(c.isdigit() for c in pw):
            raise forms.ValidationError('Mindestens 1 Zahl.')
    return pw