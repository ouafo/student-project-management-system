from django.db import models
from accounts.models import Benutzer

# Create your models here.
class Projekt(models.Model):
    name = models.CharField(max_length=200)
    beschreibung = models.TextField(blank=True)
    besitzer = models.ForeignKey(Benutzer, on_delete=models.CASCADE, related_name='projekt')
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
