from .models import SiteSettings, ContactMessage


def site_settings(request):
    return {'settings': SiteSettings.get_settings()}


def unread_messages(request):
    if request.user.is_authenticated and request.user.is_staff:
        count = ContactMessage.objects.filter(is_read=False).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}
