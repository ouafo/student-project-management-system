from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    vorname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Max', 'class': 'auth-input'}),
        label='Vorname'
    )
    nachname = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Mustermann', 'class': 'auth-input'}),
        label='Nachname'
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'z.B. max_boardify', 'class': 'auth-input'}),
        label='Benutzername'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'deine@email.de', 'class': 'auth-input'}),
        label='E-Mail'
    )
    passwort = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'auth-input'}),
        label='Passwort',
    )
    passwort_bestaetigen = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'auth-input'}),
        label='Passwort bestätigen'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Dieser Benutzername ist bereits vergeben. Bitte wähle einen anderen.')
        if ' ' in username:
            raise ValidationError('Der Benutzername darf keine Leerzeichen enthalten.')
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Diese E-Mail-Adresse ist bereits registriert.')
        return email

    def clean_passwort(self):
        pw = self.cleaned_data.get('passwort')
        if pw:
            if not any(c.isupper() for c in pw):
                raise ValidationError('Das Passwort muss mindestens 1 Großbuchstaben enthalten.')
            if not any(c.isdigit() for c in pw):
                raise ValidationError('Das Passwort muss mindestens 1 Zahl enthalten.')
        return pw

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('passwort')
        pw2 = cleaned.get('passwort_bestaetigen')
        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError('Die Passwörter stimmen nicht überein.')
        return cleaned

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['passwort'],
            first_name=self.cleaned_data['vorname'],
            last_name=self.cleaned_data.get('nachname', '')
        )
        return user