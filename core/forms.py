from django import forms
from .models import ContactMessage, Testimonial


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'country', 'job_title', 'job_details']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+44 191 515 3000'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Your Company Name'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. United Kingdom'
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. CTO, Manager, Developer'
            }),
            'job_details': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Describe your role and what you are looking for...'
            }),
        }


class TestimonialSubmitForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'company', 'content', 'rating', 'project_name']
        widgets = {
            'name':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'role':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CTO, Manager'}),
            'company':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Company'}),
            'content':      forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience with AI-Solutions…'}),
            'rating':       forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5', 'step': '0.5'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. HealthSync AI (optional)'}),
        }
