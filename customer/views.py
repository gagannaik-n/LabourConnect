from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import CustomerProfile
from .forms import CustomerProfileForm

from bookings.models import Booking


# ==================================================
# CREATE CUSTOMER PROFILE
# ==================================================

@login_required
def create_customer_profile(request):

    # Only customers can create customer profiles
    if request.user.role != 'CUSTOMER':
        return redirect('/')

    # Prevent duplicate profile
    existing_profile = CustomerProfile.objects.filter(
        user=request.user
    ).first()

    if existing_profile:
        return redirect('/customer/my-profile/')

    if request.method == 'POST':

        form = CustomerProfileForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            return redirect('/customer/my-profile/')

    else:

        form = CustomerProfileForm()

    return render(
        request,
        'customer/create_profile.html',
        {
            'form': form
        }
    )


# ==================================================
# MY CUSTOMER PROFILE
# ==================================================

@login_required
def my_customer_profile(request):

    # Only customers can access customer profile
    if request.user.role != 'CUSTOMER':
        return redirect('/')

    profile = CustomerProfile.objects.filter(
        user=request.user
    ).first()

    if not profile:
        return redirect('/customer/create-profile/')

    return render(
        request,
        'customer/my_profile.html',
        {
            'profile': profile
        }
    )


# ==================================================
# CUSTOMER DASHBOARD
# ==================================================

@login_required
def customer_dashboard(request):

    # Only customers can access customer dashboard
    if request.user.role != 'CUSTOMER':
        return redirect('/')

    customer_profile = CustomerProfile.objects.filter(
        user=request.user
    ).first()

    if not customer_profile:
        return redirect('/customer/create-profile/')

    # Get customer's bookings
    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related(
        'labor',
        'service'
    ).order_by(
        '-created_at'
    )

    # Booking counts
    total_bookings = bookings.count()

    pending_bookings = bookings.filter(
        status='PENDING'
    ).count()

    completed_bookings = bookings.filter(
        status='COMPLETED'
    ).count()

    # Recent bookings
    recent_bookings = bookings[:5]

    return render(
        request,
        'customer/dashboard.html',
        {
            'profile': customer_profile,
            'bookings': bookings,
            'recent_bookings': recent_bookings,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'completed_bookings': completed_bookings,
        }
    )