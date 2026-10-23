from django.db import models
from labor.models import LaborProfile


class Service(models.Model):

    labor = models.ForeignKey(
        LaborProfile,
        on_delete=models.CASCADE,
        related_name='services'
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
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

    def __str__(self):
        return f"{self.name} - {self.labor.full_name}"