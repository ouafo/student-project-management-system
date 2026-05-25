from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField(blank=True)
    fortschritt = models.IntegerField(default=0)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_projekte')

    def __str__(self):
        return self.titel


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

    #Sektion Benachrichtitung
    notify_email = models.BooleanField(default=True)
    notify_system = models.BooleanField(default=True)

    #Erscheinungsbild
    dark_mode = models.BooleanField(default=True)
    kompakt_modus = models.BooleanField(default=False)

    sprache = models.CharField(max_length=10, default='de') #standard_einstellung

    def __str__(self):
        return self.user.username