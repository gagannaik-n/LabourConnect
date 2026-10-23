from urllib.parse import quote_plus

from django.conf import settings
from django.db import models


class LaborProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='labor_profile'
    )

    full_name = models.CharField(
        max_length=100
    )

    profile_photo = models.ImageField(
        upload_to='labor_profiles/',
        blank=True,
        null=True
    )

    skills = models.TextField(
        blank=True
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    description = models.TextField(
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )
    latitude = models.DecimalField(
    max_digits=10,
    decimal_places=7,
    blank=True,
    null=True
)

    longitude = models.DecimalField(
    max_digits=10,
    decimal_places=7,
    blank=True,
    null=True
)

    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None

    @property
    def directions_url(self):
        """Opens Google Maps directions from the viewer's location to this laborer."""
        if self.has_coordinates:
            destination = f"{self.latitude},{self.longitude}"
        elif self.location:
            destination = quote_plus(self.location)
        else:
            return ""
        return f"https://www.google.com/maps/dir/?api=1&destination={destination}"

    def __str__(self):
        return self.full_name
