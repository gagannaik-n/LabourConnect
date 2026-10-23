from django import forms

from .models import Booking
from services.models import Service
from labor.geo import validate_lat_lng


class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking

        fields = [
            'labor',
            'service',
            'booking_date',
            'booking_time',
            'address',
            'latitude',
            'longitude',
            'notes'
        ]

        widgets = {

            'booking_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'booking_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                }
            ),

            'latitude': forms.HiddenInput(),

            'longitude': forms.HiddenInput(),

            'address': forms.Textarea(
                attrs={
                    'placeholder': 'Enter service address',
                    'rows': 3
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'placeholder': 'Additional requirements',
                    'rows': 3
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Get selected labor from the initial data
        labor_id = self.initial.get('labor')

        # If labor was selected from the labor profile page
        if labor_id:

            # Show only services belonging to that labor
            self.fields['service'].queryset = Service.objects.filter(
                labor_id=labor_id,
                is_available=True
            )

            # Hide the labor dropdown
            # The selected labor ID will still be submitted
            self.fields['labor'].widget = forms.HiddenInput()

        # If labor is selected through submitted form data
        elif self.data.get('labor'):

            self.fields['service'].queryset = Service.objects.filter(
                labor_id=self.data.get('labor'),
                is_available=True
            )

        # Otherwise show all available services
        else:

            self.fields['service'].queryset = Service.objects.filter(
                is_available=True
            )

    def clean(self):

        cleaned_data = super().clean()

        labor = cleaned_data.get('labor')
        service = cleaned_data.get('service')

        # Make sure the service belongs to the selected labor
        if labor and service:

            if service.labor_id != labor.id:

                raise forms.ValidationError(
                    'The selected service does not belong to the selected laborer.'
                )

        validate_lat_lng(
            cleaned_data.get('latitude'),
            cleaned_data.get('longitude')
        )

        return cleaned_data