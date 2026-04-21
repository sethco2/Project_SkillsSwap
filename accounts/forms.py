"""
Signup form for new users.

We extend Django's built-in UserCreationForm so we get password validation,
hashing, and the username/password1/password2 confirmation fields for free.
The only thing we add is an `email` field, which the default form skips.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # Make email required (the default User model has email but doesn't require it).
    email = forms.EmailField(required=True, help_text='We use this for password resets.')

    class Meta:
        model = User
        # Order matters — this is the order fields render in the template.
        fields = ('username', 'email', 'password1', 'password2')
