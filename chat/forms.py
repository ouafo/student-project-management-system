from django import forms
from django.contrib.auth import get_user_model
from .models import ChatNachricht

User = get_user_model()


class ChatNachrichtForm(forms.ModelForm):
    class Meta:
        model = ChatNachricht
        fields = ["empfaenger", "text"]
        widgets = {
            "empfaenger": forms.Select(
                attrs={"class": "form-control"}
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "comment-input",
                    "placeholder": "Nachricht schreiben...",
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        #  aktueller_user rausfiltern – darf sich nicht selbst schreiben
        aktueller_user = kwargs.pop("aktueller_user", None)
        super().__init__(*args, **kwargs)
        if aktueller_user is not None:
            self.fields["empfaenger"].queryset = (
                User.objects.exclude(pk=aktueller_user.pk)
            )