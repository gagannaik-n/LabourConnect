from decimal import Decimal

from django.core.exceptions import ValidationError


def validate_lat_lng(lat, lng):
    """Both values empty is fine. Otherwise both must exist and be in range."""
    if lat is None and lng is None:
        return

    if lat is None or lng is None:
        raise ValidationError('Please pick a location on the map.')

    if not (Decimal('-90') <= lat <= Decimal('90')) or \
       not (Decimal('-180') <= lng <= Decimal('180')):
        raise ValidationError('The selected map location is not valid.')
