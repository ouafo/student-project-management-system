from django.db import models
from accounts.models import Benutzer
from projekte.models import Projekt

# Create your models here.

class Aufgabe(models.Model):

    STATUS_CHOICES = [
        ('offen','Offen'),
        ('in_bearbeitung','In Bearbeitung'),
        ('in_ueberpruefung','In Überprüfung'),
        ('erledig','Erledig'),
    ]

    PRIORITAET_CHOICES = [
        ('niedrig', 'Niedrig'),
        ('mittel', 'Mittel'),
        ('hoch', 'Hoch'),
    ]

    titel = models.CharField(max_length=200)
    beschreibung = models.TextField(blank=True)
    projekt = models.ForeignKey(
        Projekt,
        on_delete=models.CASCADE,
        related_name='aufgaben'
    )
    zugewiesen_an = models.ForeignKey(
        Benutzer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='zugewiesene_aufgaben'
    )
    erstellt_von = models.ForeignKey(
        Benutzer,
        on_delete=models.CASCADE,
        related_name='erstellte_aufgaben'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='offen'
    )
    prioritaet = models.CharField(
        max_length=10,
        choices=PRIORITAET_CHOICES,
        default='mittel'
    )
    deadline = models.DateField(null=True, blank=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    aktualisiert_am = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titel

