from django import forms
from .models import CustomerProfile


class CustomerProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile

        fields = [
            'full_name',
            'profile_photo',
            'location',
            'address',
        ]

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your full name'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Bengaluru'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'placeholder': 'Enter your complete address',
                    'rows': 4
                }
            ),
        }