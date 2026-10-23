from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'customer',
        'labor',
        'service',
        'booking_date',
        'booking_time',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'booking_date',
    )

    search_fields = (
        'customer__username',
        'labor__full_name',
        'service__name',
    )

    ordering = (
        '-created_at',
    )