from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Review
from bookings.models import Booking


# ==================================================
# CREATE REVIEW
# CUSTOMER ONLY
# ==================================================

@login_required
def create_review(request, booking_id):

    # Only customers can create reviews
    if request.user.role != 'CUSTOMER':
        return redirect('/')

    # Get only the customer's booking
    booking = Booking.objects.filter(
        id=booking_id,
        customer=request.user
    ).select_related(
        'labor',
        'service'
    ).first()

    # Booking does not exist or does not belong to customer
    if not booking:
        return redirect('/bookings/my-bookings/')

    # Review can only be submitted after work is completed
    if booking.status != 'COMPLETED':
        return redirect('/bookings/my-bookings/')

    # Prevent duplicate review
    existing_review = Review.objects.filter(
        booking=booking
    ).first()

    if existing_review:
        return redirect('/bookings/my-bookings/')

    # Submit review
    if request.method == 'POST':

        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        try:
            rating = int(rating)
        except (TypeError, ValueError):
            rating = 0

        # Validate rating
        if rating < 1 or rating > 5:

            return render(
                request,
                'reviews/create_review.html',
                {
                    'booking': booking,
                    'error': 'Rating must be between 1 and 5.'
                }
            )

        # Create review
        Review.objects.create(
            customer=request.user,
            labor=booking.labor,
            booking=booking,
            rating=rating,
            comment=comment
        )

        return redirect('/bookings/my-bookings/')

    return render(
        request,
        'reviews/create_review.html',
        {
            'booking': booking
        }
    )