from django.contrib import admin
from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'location',
        'created_at',
    )

    search_fields = (
        'full_name',
        'location',
    )