from .models import Notification

def projekte_notifications(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        latest = Notification.objects.filter(user=request.user)[:5]
        return {
            'unread_count': count,
            'notifications_list': latest
        }
    return {'unread_count': 0, 'notifications_list': []}