"""
Views for the accounts app.

Function-based view (FBV) for user registration. After a successful signup
we log the user in automatically and redirect them to their dashboard,
which is a friendlier flow than making them log in twice.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import SignUpForm


def register(request):
    """Handle GET (show empty form) and POST (create user) for signup."""
    if request.method == 'POST':
        # Bind the form to the submitted data so we can validate it.
        form = SignUpForm(request.POST)
        if form.is_valid():
            # form.save() creates a real User row with a hashed password.
            user = form.save()
            # Log the new user in immediately (no need for a second visit).
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account is ready.')
            # Names like 'dashboard' are URL-pattern names, defined later.
            return redirect('dashboard')
    else:
        # GET request — just hand back an empty form.
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})
