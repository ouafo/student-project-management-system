
from django.conf import settings
from django.db import models

from projekte.models import Projekt


class ChatNachricht(models.Model):
    projekt = models.ForeignKey(
    'projekte.projekt',
        on_delete=models.CASCADE,
        related_name="nachrichten"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gesendete_nachrichten"
    )

    text = models.TextField(max_length=1000)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["erstellt_am"]

    def __str__(self):
        return f"{self.sender.username} → {self.projekt.titel}: {self.text[:40]}"