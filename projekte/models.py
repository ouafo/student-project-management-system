from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField(blank=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_projekte')
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
        erledigt = alle_aufgaben.filter(status=Aufgabe.Status.ERLEDIGT).count()
        return round((erledigt / gesamt) * 100)

    @property
    def erledigte_aufgaben_zaehlen(self):
        from aufgaben.models import Aufgabe
        return self.aufgaben.filter(status=Aufgabe.Status.ERLEDIGT).count()

    @property
    def aufgaben_gesamt(self):
        return self.aufgaben.count()


class Mitgliedschaft(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mitgliedschaften')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='mitgliedschaft_set')
    beigetreten_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} -> {self.project.titel}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_bild = models.ImageField(upload_to='avatars/', null=True, blank=True)
    avatar_farbe = models.CharField(max_length=20, default='#3b82f6')
    profil_oeffentlich = models.BooleanField(default=True)
    in_teilnehmerliste_auffindbar = models.BooleanField(default=True)
    notify_email = models.BooleanField(default=True)
    notify_system = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projekt_notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    notify_projekt = models.BooleanField(default=False)
    notify_deadline = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']


def send_notification(user, title, message, notification_type):
    if hasattr(user, 'profile'):
        profile = user.profile
        if profile.notify_system:
            Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type
            )
        if profile.notify_email:
            from django.core.mail import send_mail
            send_mail(
                subject=f"Boardify: {title}",
                message=f"Hallo,\n\n{message}\n\nViele Grüße\nDein Boardify-Team",
                from_email='noreply@boardify.de',
                recipient_list=[user.email],
                fail_silently=True,
            )