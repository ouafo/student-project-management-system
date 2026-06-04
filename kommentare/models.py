
from django.conf import settings
from django.db import models
from aufgaben.models import Aufgabe

class Kommentar(models.Model):
    aufgabe = models.ForeignKey(
        Aufgabe,
        on_delete=models.CASCADE,
        related_name="kommentare"
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["erstellt_am"]

    def __str__(self):
        return f"Kommentar von {self.autor} zu {self.aufgabe}"
