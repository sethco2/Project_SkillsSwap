from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Your name",
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control", "placeholder": "you@example.com",
    }))
    subject = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Subject (optional)",
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control", "rows": 5, "placeholder": "Tell me what you're working on.",
    }))
    # Honeypot — bots fill this; humans don't see it.
    website = forms.CharField(required=False, widget=forms.HiddenInput())
