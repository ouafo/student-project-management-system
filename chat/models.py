
from django.conf import settings
from django.db import models

class ChatNachricht(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gesendete_chat_nachrichten"
    )
    empfaenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="erhaltene_chat_nachrichten"
    )
    text = models.TextField()
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["erstellt_am"]

    def __str__(self):
        return f"{self.sender} → {self.empfaenger}"