from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service

        fields = [
            'name',
            'description',
            'price',
            'is_available',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Plumbing'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe your service',
                    'rows': 4
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'min': '0'
                }
            ),
        }