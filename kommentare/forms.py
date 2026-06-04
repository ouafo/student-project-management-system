from django import forms
from .models import Kommentar


class KommentarForm(forms.ModelForm):
    class Meta:
        model = Kommentar
        fields = ["text"]
        widgets = {
            # Fix #8 aus letztem Review: Textarea statt TextInput
            "text": forms.Textarea(
                attrs={
                    "class": "kommentar-input",
                    "placeholder": "Kommentar hinzufügen...",
                    "rows": 3,
                }
            )
        }
        labels = {
            "text": ''
        }