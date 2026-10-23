from django.conf import settings


def google_maps(request):
    """Makes the Google Maps API key available in every template."""
    return {"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY}
