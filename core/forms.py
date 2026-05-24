from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+977 98XXXXXXXX (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'How can we help?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5,
                'placeholder': 'Tell us about your project or question...'
            }),
        }
