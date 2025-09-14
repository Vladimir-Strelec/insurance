from django import forms
from .models import InsuranceLead


class LeadForm(forms.ModelForm):
    class Meta:
        model = InsuranceLead
        fields = ['full_name', 'email', 'phone', 'message']
        labels = {
            'full_name': 'Vollständiger Name',
            'email': 'E-Mail',
            'phone': 'Telefonnummer',
            'message': 'Nachricht',
        }
        error_messages = {
            'full_name': {
                'required': 'Bitte geben Sie Ihren vollständigen Namen ein.',
            },
            'email': {
                'required': 'Bitte geben Sie Ihre E-Mail-Adresse ein.',
                'invalid': 'Bitte geben Sie eine gültige E-Mail-Adresse ein.',
            },
            'phone': {
                'required': 'Bitte geben Sie Ihre Telefonnummer ein.',
            },
            'message': {
                'required': 'Bitte schreiben Sie eine Nachricht.',
            },
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full rounded-md border border-gray-300 p-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full rounded-md border border-gray-300 p-2'}),
            'phone': forms.TextInput(attrs={'class': 'w-full rounded-md border border-gray-300 p-2'}),
            'message': forms.Textarea(attrs={'class': 'w-full rounded-md border border-gray-300 p-2', 'rows': 4}),
        }
