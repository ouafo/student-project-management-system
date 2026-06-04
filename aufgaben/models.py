from django.conf import settings
from django.db import models
from django.urls import reverse
from projekte.models import Projekt


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
    beschreibung = models.TextField(blank=True)
    #  Projekt ForeignKey behalten!
    projekt = models.ForeignKey(
        Projekt,
        on_delete=models.CASCADE,
        related_name='aufgaben',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.OFFEN
    )
    prioritaet = models.CharField(
        max_length=20,
        choices=Prioritaet.choices,
        default=Prioritaet.MITTEL
    )
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
    aktualisiert_am = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titel

    def get_absolute_url(self):
        return reverse("aufgabe_detail", kwargs={"pk": self.pk})

