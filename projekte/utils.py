from django.core.mail import send_mail
from .models import Notification


def send_notification(user, title, message, notification_type):
    """
    Universelle Funktion für System- und E-Mail-Benachrichtigungen.
    Prüft die Einstellungen im Benutzerprofil.
    """
    # Überprüfen, ob das Profil existiert (Sicherheitsanker)
    if hasattr(user, 'profile'):
        profile = user.profile

        # 1. System-Benachrichtigung (Glocke in der Sidebar)
        if profile.notify_system:
            Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type
            )

        # 2. E-Mail-Benachrichtigung
        if profile.notify_email:
            send_mail(
                subject=f"Boardify: {title}",
                message=f"Hallo,\n\n{message}\n\nViele Grüße\nDein Boardify-Team",
                from_email='noreply@boardify.de',
                recipient_list=[user.email],
                fail_silently=True,
            )