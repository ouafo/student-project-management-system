from django import forms
from django.contrib.auth import get_user_model
from .models import Aufgabe, Kommentar, ChatNachricht

User = get_user_model()


class AufgabeForm(forms.ModelForm):
    class Meta:
        model = Aufgabe
        fields = [
            "titel",
            "beschreibung",
            "status",
            "prioritaet",
            "zugewiesen_an",
            "deadline",
        ]
        widgets = {
            "titel": forms.TextInput(attrs={"class": "form-control"}),
            "beschreibung": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "prioritaet": forms.Select(attrs={"class": "form-control"}),
            "zugewiesen_an": forms.Select(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class KommentarForm(forms.ModelForm):
    class Meta:
        model = Kommentar
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(
                attrs={
                    "class": "comment-input",
                    "placeholder": "Kommentar hinzufügen..."
                }
            )
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Aufgabe
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"})
        }


class ChatNachrichtForm(forms.ModelForm):
    class Meta:
        model = ChatNachricht
        fields = ["empfaenger", "text"]
        widgets = {
            "empfaenger": forms.Select(attrs={"class": "form-control"}),
            "text": forms.TextInput(
                attrs={
                    "class": "comment-input",
                    "placeholder": "Nachricht schreiben..."
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        aktueller_user = kwargs.pop("aktueller_user", None)
        super().__init__(*args, **kwargs)
        if aktueller_user is not None:
            self.fields["empfaenger"].queryset = User.objects.exclude(pk=aktueller_user.pk)