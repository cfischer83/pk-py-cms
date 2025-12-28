from django.conf import settings
from apps.content.models import Page


def site_settings(request):
    """Add site-wide settings to template context."""
    return {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'menu_pages': Page.objects.filter(
            status=Page.Status.PUBLISHED,
            show_in_menu=True
        ).order_by('menu_order'),
    }
