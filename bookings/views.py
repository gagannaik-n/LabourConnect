from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Booking
from .forms import BookingForm

from labor.models import LaborProfile


# ==================================================
# CREATE BOOKING
# CUSTOMER ONLY
# ==================================================

@login_required
def create_booking(request):

    # Only customers can create bookings
    if request.user.role != 'CUSTOMER':
        return redirect('/')

    labor_id = request.GET.get('labor')

    if request.method == 'POST':

        form = BookingForm(
            request.POST,
            initial={'labor': labor_id}
        )

        if form.is_valid():

            booking = form.save(commit=False)

            booking.customer = request.user

            booking.save()

            return redirect('/bookings/my-bookings/')

    else:

        form = BookingForm(
            initial={'labor': labor_id}
        )

    return render(
        request,
        'bookings/create_booking.html',
        {
            'form': form
        }
    )


# ==================================================
# CUSTOMER BOOKING LIST
# CUSTOMER ONLY
# ==================================================

@login_required
def booking_list(request):

    # Only customers can access customer bookings
    if request.user.role != 'CUSTOMER':
        return redirect('/')

    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related(
        'labor',
        'service'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'bookings/booking_list.html',
        {
            'bookings': bookings
        }
    )


# ==================================================
# LABOR BOOKING LIST
# LABOR ONLY
# ==================================================

@login_required
def labor_booking_list(request):

    # Only labor users can access customer bookings
    if request.user.role != 'LABOR':
        return redirect('/')

    labor_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if not labor_profile:
        return redirect('/')

    bookings = Booking.objects.filter(
        labor=labor_profile
    ).select_related(
        'customer',
        'service'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'bookings/labor_booking_list.html',
        {
            'bookings': bookings
        }
    )


# ==================================================
# CANCEL BOOKING
# CUSTOMER ONLY
# ==================================================

@login_required
@require_POST
def cancel_booking(request, booking_id):

    # Only customers can cancel bookings
    if request.user.role != 'CUSTOMER':
        return redirect('/')

    booking = Booking.objects.filter(
        id=booking_id,
        customer=request.user
    ).first()

    if booking and booking.status == 'PENDING':

        booking.status = 'CANCELLED'

        booking.save()

    return redirect('/bookings/my-bookings/')


# ==================================================
# BOOKING DETAIL
# CUSTOMER OR ASSIGNED LABOR
# ==================================================

def _booking_detail_context(booking, viewer_is_labor):

    # Pins for the Google Map: customer's service location + laborer's location
    map_markers = []

    if booking.has_coordinates:
        map_markers.append({
            'lat': float(booking.latitude),
            'lng': float(booking.longitude),
            'title': booking.address[:80],
            'kind': 'customer',
        })

    if booking.labor.has_coordinates:
        map_markers.append({
            'lat': float(booking.labor.latitude),
            'lng': float(booking.labor.longitude),
            'title': booking.labor.full_name,
            'kind': 'labor',
        })

    # Laborer navigates to the customer; customer navigates to the laborer
    if viewer_is_labor:
        directions_url = booking.directions_url
    else:
        directions_url = booking.labor.directions_url

    return {
        'booking': booking,
        'map_markers': map_markers,
        'directions_url': directions_url,
        'viewer_is_labor': viewer_is_labor,
    }


@login_required
def booking_detail(request, booking_id):

    booking = Booking.objects.filter(
        id=booking_id
    ).select_related(
        'labor',
        'service',
        'customer'
    ).first()

    if not booking:
        return redirect('/')

    # Customer can see their own booking
    if (
        request.user.role == 'CUSTOMER'
        and booking.customer == request.user
    ):

        return render(
            request,
            'bookings/booking_detail.html',
            _booking_detail_context(booking, viewer_is_labor=False)
        )

    # Assigned labor can see the booking
    if (
        request.user.role == 'LABOR'
        and booking.labor.user == request.user
    ):

        return render(
            request,
            'bookings/booking_detail.html',
            _booking_detail_context(booking, viewer_is_labor=True)
        )

    # Everyone else is denied
    return redirect('/')


# ==================================================
# ACCEPT BOOKING
# LABOR ONLY
# ==================================================

@login_required
@require_POST
def accept_booking(request, booking_id):

    # Only labor can accept bookings
    if request.user.role != 'LABOR':
        return redirect('/')

    booking = Booking.objects.filter(
        id=booking_id,
        labor__user=request.user
    ).first()

    if booking and booking.status == 'PENDING':

        booking.status = 'ACCEPTED'

        booking.save()

    return redirect('/bookings/labor-bookings/')


# ==================================================
# REJECT BOOKING
# LABOR ONLY
# ==================================================

@login_required
@require_POST
def reject_booking(request, booking_id):

    # Only labor can reject bookings
    if request.user.role != 'LABOR':
        return redirect('/')

    booking = Booking.objects.filter(
        id=booking_id,
        labor__user=request.user
    ).first()

    if booking and booking.status == 'PENDING':

        booking.status = 'REJECTED'

        booking.save()

    return redirect('/bookings/labor-bookings/')


# ==================================================
# START WORK
# LABOR ONLY
# ==================================================

@login_required
@require_POST
def start_booking(request, booking_id):

    # Only labor can start work
    if request.user.role != 'LABOR':
        return redirect('/')

    booking = Booking.objects.filter(
        id=booking_id,
        labor__user=request.user
    ).first()

    if booking and booking.status == 'ACCEPTED':

        booking.status = 'IN_PROGRESS'

        booking.save()

    return redirect('/bookings/labor-bookings/')


# ==================================================
# COMPLETE WORK
# LABOR ONLY
# ==================================================

@login_required
@require_POST
def complete_booking(request, booking_id):

    # Only labor can complete work
    if request.user.role != 'LABOR':
        return redirect('/')

    booking = Booking.objects.filter(
        id=booking_id,
        labor__user=request.user
    ).first()

    if booking and booking.status == 'IN_PROGRESS':

        booking.status = 'COMPLETED'

        booking.save()

    return redirect('/bookings/labor-bookings/')