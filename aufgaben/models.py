from django.conf import settings
from django.db import models
from django.urls import reverse


class Aufgabe(models.Model):
    class Status(models.TextChoices):
        OFFEN = "offen", "Offen"
        IN_BEARBEITUNG = "in_bearbeitung", "In Bearbeitung"
        IN_UEBERPRUEFUNG = "in_ueberpruefung", "In Überprüfung"
        ERLEDIGT = "erledigt", "Erledigt"

    class Prioritaet(models.TextChoices):
        NIEDRIG = "niedrig", "Niedrig"
        MITTEL = "mittel", "Mittel"
        HOCH = "hoch", "Hoch"

    titel = models.CharField(max_length=200)
    beschreibung = models.TextField()
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.OFFEN)
    prioritaet = models.CharField(max_length=20, choices=Prioritaet.choices, default=Prioritaet.MITTEL)

    zugewiesen_an = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="zugewiesene_aufgaben"
    )
    erstellt_von = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="erstellte_aufgaben"
    )

    erstellt_am = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titel

    def get_absolute_url(self):
        return reverse("aufgaben:aufgabe_detail", kwargs={"pk": self.pk})


class Kommentar(models.Model):
    aufgabe = models.ForeignKey(Aufgabe, on_delete=models.CASCADE, related_name="kommentare")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["erstellt_am"]

    def __str__(self):
        return f"Kommentar von {self.autor} zu {self.aufgabe}"


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
        return f"{self.sender} -> {self.empfaenger}"