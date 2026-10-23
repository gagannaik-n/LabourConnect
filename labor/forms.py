from django import forms
from .models import LaborProfile
from .geo import validate_lat_lng


class LaborProfileForm(forms.ModelForm):

    class Meta:
        model = LaborProfile

        fields = [
            'full_name',
            'profile_photo',
            'skills',
            'experience_years',
            'description',
            'location',
            'latitude',
            'longitude',
            'hourly_rate',
            'is_available',
        ]

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your full name'
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'placeholder': 'Example: Plumbing, Pipe Repair',
                    'rows': 3
                }
            ),

            'experience_years': forms.NumberInput(
                attrs={
                    'min': 0
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe your experience and services',
                    'rows': 4
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Bengaluru'
                }
            ),

            'latitude': forms.HiddenInput(),

            'longitude': forms.HiddenInput(),

            'hourly_rate': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'min': '0'
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        validate_lat_lng(
            cleaned_data.get('latitude'),
            cleaned_data.get('longitude')
        )

        return cleaned_data
