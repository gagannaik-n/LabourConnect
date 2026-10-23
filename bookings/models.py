from urllib.parse import quote_plus

from django.conf import settings
from django.db import models
from labor.models import LaborProfile
from services.models import Service


class Booking(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_bookings'
    )

    labor = models.ForeignKey(
        LaborProfile,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_date = models.DateField()

    booking_time = models.TimeField()

    address = models.TextField()

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

    notes = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
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
        """Google Maps directions to the customer's service location."""
        if self.has_coordinates:
            destination = f"{self.latitude},{self.longitude}"
        elif self.address:
            destination = quote_plus(self.address)
        else:
            return ""
        return f"https://www.google.com/maps/dir/?api=1&destination={destination}"

    def __str__(self):
        return f"{self.customer.username} - {self.service.name}"