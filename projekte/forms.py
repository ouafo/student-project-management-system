from django import forms
from accounts.models import Benutzer
from .models import Projekt


class ProjectForm(forms.ModelForm):
    teilnehmer = forms.ModelMultipleChoiceField(
        queryset=Benutzer.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Teilnehmer einladen"
    )
    fortschritt = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=0,
        required=False
    )

    class Meta:
        model = Projekt          # ← Projekt statt Project!
        fields = ['titel', 'beschreibung', 'fortschritt']


class ProfilForm(forms.Form):
    vorname = forms.CharField(
        max_length=50,
        label='Vorname',
        widget=forms.TextInput(attrs={
            'placeholder': 'Vorname',
            'class': 'f-input'
        }),
    )
    nachname = forms.CharField(
        max_length=50,
        required=False,
        label='Nachname',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nachname',
            'class': 'f-input'
        }),
    )
    email = forms.EmailField(
        label='E-Mail',
        widget=forms.TextInput(attrs={
            'placeholder': 'E-Mail Adresse',
            'class': 'f-input'
        }),
    )


class PasswortForm(forms.Form):
    altes_passwort = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '........',
            'class': 'f-input'
        }),
        label='Aktuelles Passwort'
    )
    neues_passwort = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Neues Passwort',
            'class': 'f-input'
        }),
        label='Neues Passwort',
        min_length=8
    )
    passwort_bestaetigen = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Passwort wiederholen',
            'class': 'f-input'
        }),
    )

    def clean(self):
        cleaned = super().clean()
        alt = cleaned.get('altes_passwort')
        neu = cleaned.get('neues_passwort')
        bestaetigen = cleaned.get('passwort_bestaetigen')

        if neu and bestaetigen and neu != bestaetigen:
            raise forms.ValidationError(
                "Die Passwörter stimmen nicht überein."
            )
        if alt and neu and alt == neu:
            raise forms.ValidationError(
                "Das neue Passwort darf nicht mit dem aktuellen identisch sein."
            )
        return cleaned