from django.contrib import admin
from .models import LaborProfile


@admin.register(LaborProfile)
class LaborProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'experience_years',
        'hourly_rate',
        'location',
        'is_available',
    )

    list_filter = (
        'is_available',
    )

    search_fields = (
        'full_name',
        'skills',
        'location',
    )   