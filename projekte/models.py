from django.db import models
from django.conf import settings


class Projekt(models.Model):
    """Vereintes Projekt Model"""
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField(blank=True)
    fortschritt = models.IntegerField(default=0)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_projekte'
    )
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titel


class Mitgliedschaft(models.Model):
    """Benutzer Mitgliedschaft in einem Projekt"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mitgliedschaften'
    )
    projekt = models.ForeignKey(
        Projekt,
        on_delete=models.CASCADE,
        related_name='mitgliedschaft_set'
    )
    beigetreten_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'projekt')

    def __str__(self):
        return f"{self.user.username} → {self.projekt.titel}"


class Profile(models.Model):
    """Benutzer Profil"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    avatar_bild = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    avatar_farbe = models.CharField(
        max_length=20,
        default='#3b82f6'
    )
    # Benachrichtigungen
    notify_email = models.BooleanField(default=True)
    notify_system = models.BooleanField(default=True)
    # Erscheinungsbild
    dark_mode = models.BooleanField(default=False)
    kompakt_modus = models.BooleanField(default=False)
    sprache = models.CharField(max_length=10, default='de')

    def __str__(self):
        return self.user.username