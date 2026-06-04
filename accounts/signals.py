from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Lazy Import – vermeidet circular import
        from projekte.models import Profile
        Profile.objects.get_or_create(user=instance)