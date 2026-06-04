from django import forms
from django.contrib.auth import get_user_model
from .models import Aufgabe

User = get_user_model()


class AufgabeForm(forms.ModelForm):
    class Meta:
        model = Aufgabe
        fields = [
            "titel", "beschreibung", "projekt",
            "status", "prioritaet", "zugewiesen_an", "deadline",
        ]
        widgets = {
            "titel":         forms.TextInput(attrs={"class": "form-control"}),
            "beschreibung":  forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "projekt":       forms.Select(attrs={"class": "form-control"}),
            "status":        forms.Select(attrs={"class": "form-control"}),
            "prioritaet":    forms.Select(attrs={"class": "form-control"}),
            "zugewiesen_an": forms.Select(attrs={"class": "form-control"}),
            "deadline":      forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        # ✅ Fix #4 + #5: User und Projekt filtern
        aktueller_user = kwargs.pop('aktueller_user', None)
        projekt        = kwargs.pop('projekt', None)
        super().__init__(*args, **kwargs)
        self.fields['projekt'].required = False

        if aktueller_user:
            from projekte.models import Mitgliedschaft
            eigene_projekte = Mitgliedschaft.objects.filter(
                user=aktueller_user
            ).values_list('projekt_id', flat=True)
            self.fields['projekt'].queryset = (
                Aufgabe._meta.get_field('projekt')
                .related_model.objects.filter(id__in=eigene_projekte)
            )

        if projekt:
            from projekte.models import Mitgliedschaft
            mitglieder_ids = Mitgliedschaft.objects.filter(
                projekt=projekt
            ).values_list('user_id', flat=True)
            self.fields['zugewiesen_an'].queryset = (
                User.objects.filter(id__in=mitglieder_ids)
            )


class StatusForm(forms.ModelForm):
    class Meta:
        model = Aufgabe
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"})
        }
