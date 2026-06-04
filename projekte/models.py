from django.db import models
from django.conf import settings


class Projekt(models.Model):
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField(blank=True)
    fortschritt = models.IntegerField(default=0)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_projekte'
    )
    projekte_oeffentlich = models.BooleanField(default=False)
    nur_mitgliederzugriff = models.BooleanField(default=True)

    def __str__(self):
        return self.titel

    @property
    def berechne_fortschritt(self):
        from aufgaben.models import Aufgabe
        alle_aufgaben = self.aufgaben.all()
        gesamt = alle_aufgaben.count()
        if gesamt == 0:
            return 0
        erledigt = alle_aufgaben.filter(
            status=Aufgabe.Status.ERLEDIGT
        ).count()
        return round((erledigt / gesamt) * 100)

    @property
    def erledigte_aufgaben_zaehlen(self):
        from aufgaben.models import Aufgabe
        return self.aufgaben.filter(
            status=Aufgabe.Status.ERLEDIGT
        ).count()

    @property
    def aufgaben_gesamt(self):
        return self.aufgaben.count()


class Mitgliedschaft(models.Model):
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
    profil_oeffentlich = models.BooleanField(default=True)
    in_teilnehmerliste_auffindbar = models.BooleanField(default=True)
    notify_email = models.BooleanField(default=True)
    notify_system = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    kompakt_modus = models.BooleanField(default=False)
    sprache = models.CharField(max_length=10, default='de')

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('aufgabe', 'Neue Aufgabe'),
        ('deadline', 'Deadline nähert sich'),
        ('projekt', 'Projekt-Update'),
        ('system', 'System-Mitteilung'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projekt_notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notify_projekt = models.BooleanField(default=False)
    notify_deadline = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"