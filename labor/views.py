from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LaborProfileForm
from .models import LaborProfile
from django.db.models import Q, Avg


# ==================================================
# CREATE LABOR PROFILE
# ==================================================

@login_required
def create_labor_profile(request):

    # Only LABOR users can create labor profile
    if request.user.role != 'LABOR':
        return redirect('/')

    existing_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if existing_profile:
        return redirect(
            'labor_detail',
            labor_id=existing_profile.id
        )

    if request.method == 'POST':

        form = LaborProfileForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            labor_profile = form.save(
                commit=False
            )

            labor_profile.user = request.user

            labor_profile.save()

            return redirect(
                'labor_detail',
                labor_id=labor_profile.id
            )

    else:

        form = LaborProfileForm()

    return render(
        request,
        'labor/create_profile.html',
        {
            'form': form
        }
    )


# ==================================================
# EDIT LABOR PROFILE (including map location)
# ==================================================

@login_required
def edit_labor_profile(request):

    # Only LABOR users can edit labor profile
    if request.user.role != 'LABOR':
        return redirect('/')

    labor_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if not labor_profile:
        return redirect('create_labor_profile')

    if request.method == 'POST':

        form = LaborProfileForm(
            request.POST,
            request.FILES,
            instance=labor_profile
        )

        if form.is_valid():

            form.save()

            return redirect(
                'labor_detail',
                labor_id=labor_profile.id
            )

    else:

        form = LaborProfileForm(
            instance=labor_profile
        )

    return render(
        request,
        'labor/create_profile.html',
        {
            'form': form,
            'editing': True
        }
    )


# ==================================================
# LABOR LIST
# ==================================================

def labor_list(request):

    search = request.GET.get(
        'search',
        ''
    ).strip()

    laborers = LaborProfile.objects.filter(
        is_available=True
    )

    if search:

        laborers = laborers.filter(
            Q(full_name__icontains=search) |
            Q(skills__icontains=search) |
            Q(location__icontains=search)
        )

    laborers = laborers.annotate(
        average_rating=Avg('reviews__rating')
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'labor/labor_list.html',
        {
            'laborers': laborers,
            'search': search
        }
    )


# ==================================================
# LABOR DETAIL
# ==================================================

def labor_detail(request, labor_id):

    labor = LaborProfile.objects.get(
        id=labor_id,
        is_available=True
    )

    reviews = labor.reviews.select_related(
        'customer'
    ).order_by(
        '-created_at'
    )

    average_rating = reviews.aggregate(
        average=Avg('rating')
    )['average']

    review_count = reviews.count()

    # Pin shown on the Google Map (only if the laborer set a location)
    map_markers = []

    if labor.has_coordinates:
        map_markers.append({
            'lat': float(labor.latitude),
            'lng': float(labor.longitude),
            'title': labor.full_name,
            'kind': 'labor',
        })

    return render(
        request,
        'labor/labor_detail.html',
        {
            'labor': labor,
            'reviews': reviews,
            'average_rating': average_rating,
            'review_count': review_count,
            'map_markers': map_markers,
        }
    )


# ==================================================
# MY LABOR PROFILE
# ==================================================

@login_required
def my_labor_profile(request):

    # Only LABOR users can access labor profile
    if request.user.role != 'LABOR':
        return redirect('/')

    labor_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if not labor_profile:
        return redirect(
            'create_labor_profile'
        )

    return redirect(
        'labor_detail',
        labor_id=labor_profile.id
    )


# ==================================================
# LABOR DASHBOARD
# ==================================================

@login_required
def labor_dashboard(request):

    # Only LABOR users can access labor dashboard
    if request.user.role != 'LABOR':
        return redirect('/')

    labor_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if not labor_profile:
        return redirect(
            'create_labor_profile'
        )

    from bookings.models import Booking

    bookings = Booking.objects.filter(
        labor=labor_profile
    ).select_related(
        'customer',
        'service'
    ).order_by(
        '-created_at'
    )

    # Booking counts
    total_bookings = bookings.count()

    pending_bookings = bookings.filter(
        status='PENDING'
    ).count()

    accepted_bookings = bookings.filter(
        status='ACCEPTED'
    ).count()

    completed_bookings = bookings.filter(
        status='COMPLETED'
    ).count()

    return render(
        request,
        'labor/dashboard.html',
        {
            'profile': labor_profile,
            'bookings': bookings,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'accepted_bookings': accepted_bookings,
            'completed_bookings': completed_bookings,
        }
    )