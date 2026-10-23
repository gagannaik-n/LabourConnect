
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import logout_view


def home(request):
    return render(request, 'home.html')


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Language switching: English / Kannada
    path('i18n/', include('django.conf.urls.i18n')),

    # Accounts
    path('accounts/', include('accounts.urls')),
    path('accounts/logout/', logout_view, name='logout'),

    # Labor
    path('labor/', include('labor.urls')),

    # Customer
    path('customer/', include('customer.urls')),

    # Services
    path('services/', include('services.urls')),

    # Bookings
    path('bookings/', include('bookings.urls')),

    # Reviews
    path('reviews/', include('reviews.urls')),
]


# Media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )