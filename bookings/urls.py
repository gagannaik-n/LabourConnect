from django.urls import path
from . import views


urlpatterns = [
    path(
        'create/',
        views.create_booking,
        name='create_booking'
    ),

    path(
        'my-bookings/',
        views.booking_list,
        name='booking_list'
    ),

    path(
        'labor-bookings/',
        views.labor_booking_list,
        name='labor_booking_list'
    ),

    path(
        'accept/<int:booking_id>/',
        views.accept_booking,
        name='accept_booking'
    ),

    path(
        'reject/<int:booking_id>/',
        views.reject_booking,
        name='reject_booking'
    ),

    path(
    'start/<int:booking_id>/',
    views.start_booking,
    name='start_booking'
    ),

    path(
    'complete/<int:booking_id>/',
    views.complete_booking,
    name='complete_booking'
    ),

    path(
    'cancel/<int:booking_id>/',
    views.cancel_booking,
    name='cancel_booking'
    ),

    path(
    'detail/<int:booking_id>/',
    views.booking_detail,
    name='booking_detail'
    ),
]