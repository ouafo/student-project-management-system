from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Benutzer(AbstractUser):

    profilbild = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username