from .models import SiteSettings


def site_settings(request):
    """Makes site settings available in every template as {{ settings }}."""
    return {'settings': SiteSettings.get_settings()}
