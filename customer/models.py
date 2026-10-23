from django.conf import settings
from django.db import models


class CustomerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )

    full_name = models.CharField(
        max_length=100
    )

    profile_photo = models.ImageField(
        upload_to='customer_profiles/',
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.full_name