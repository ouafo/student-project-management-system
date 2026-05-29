from django import forms
from django.contrib.auth.models import User
from .models import Project


class ProjectForm(forms.ModelForm):
    teilnehmer = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
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
        model = Project
        fields = ['titel', 'beschreibung', 'fortschritt']
        """labels = {
            'titel': 'Projektname',
            'beschreibung': 'Beschreibung',
        }
        widgets = {
            'titel': forms.TextInput(attrs={'placeholder': 'z.B. Design einer Website'}),
            'beschreibung': forms.Textarea(attrs={'placeholder': 'Beschreibe kurz dein Projekt', 'rows': 3}),
        }"""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Es werden nur User angezeigt, deren Profil das erlaubt
            self.fields['teilnehmer'].queryset = User.objects.filter(
                profile__in_teilnehmerliste_auffindbar=True
            )

class ProfilForm(forms.Form):
    vorname = forms.CharField(
        max_length=50,
        label = 'Vorname',
        widget=forms.TextInput(attrs={'placeholder': 'Vorname',
                                      'class': 'f-input'}),
    )
    nachname = forms.CharField(
        max_length=50,
        required=False,
        label = 'Nachname',
        widget=forms.TextInput(attrs={'placeholder': 'Nachname',
                                      'class': 'f-input'}),
    )
    email = forms.EmailField(
        label='E-Mail',
        widget=forms.TextInput(attrs={'placeholder': 'E-Mail Adresse',
                                      'class': 'f-input'}),
    )

class PasswortForm(forms.Form):
    altes_passwort = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '........',
                                          'class': 'f-input'}),
        label = 'Aktuelles Passwort'
    )
    neues_passwort = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Neues Passwort',
                                          'class': 'f-input'}),
        label = 'Neues Passwort',
        min_length=8
    )
    passwort_bestaetigen = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Passwort wiederholen',
                                          'class': 'f-input'}),
    )


    def clean(self):
        cleaned = super().clean()
        alt = cleaned.get('altes_passwort')
        neu = cleaned.get('neues_passwort')
        bestaetigen = cleaned.get('passwort_bestaetigen')

        # Stimmen neu und Bestätigung überein?
        if neu and bestaetigen and neu != bestaetigen:
            raise forms.ValidationError("Die Passwörter stimmen nicht überein.")

        # 2.Ist das neue Passwort identisch mit dem alten?
        if alt and neu and alt == neu:
            raise forms.ValidationError("Das neue Passwort darf nicht mit dem aktuellen identisch sein.")

        return cleaned