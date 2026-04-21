"""
Function-based views for the Skills app.

Each view receives `request` (and any URL captures) and returns an
HttpResponse — usually via render() (HTML page) or redirect() (302).
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import Skill
from .forms import SkillForm


# --------------------------------------------------------------------------
# Public views (no login required)
# --------------------------------------------------------------------------

def skill_list(request):
    """Browse all available skills, with a simple search box."""
    # Only show available skills to the public — owners can still see their
    # hidden ones from the dashboard.
    qs = Skill.objects.filter(is_available=True).select_related('owner')

    # Optional search query (?q=python)
    query = request.GET.get('q', '').strip()
    if query:
        # Q-objects let us OR multiple fields together.
        qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # Optional category filter (?category=tutoring)
    category = request.GET.get('category', '')
    if category:
        qs = qs.filter(category=category)

    context = {
        'skills': qs,
        'query': query,
        'category': category,
        'categories': Skill.CATEGORY_CHOICES,
    }
    return render(request, 'skills/skill_list.html', context)


def skill_detail(request, pk):
    """Show one skill in detail. 404 if it doesn't exist."""
    # get_object_or_404 is the safe shortcut: raises 404 instead of crashing.
    skill = get_object_or_404(Skill, pk=pk)
    return render(request, 'skills/skill_detail.html', {'skill': skill})


# --------------------------------------------------------------------------
# Owner-only / logged-in views
# --------------------------------------------------------------------------

@login_required  # Bounces anonymous visitors to LOGIN_URL ('login')
def skill_create(request):
    """Create a new skill post owned by the current user."""
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            # commit=False builds the object but doesn't INSERT yet,
            # so we can attach the owner before saving.
            skill = form.save(commit=False)
            skill.owner = request.user      # <-- security-critical line
            skill.save()
            messages.success(request, 'Skill posted!')
            return redirect(skill)          # uses get_absolute_url()
    else:
        form = SkillForm()

    return render(request, 'skills/skill_form.html', {'form': form, 'is_edit': False})


@login_required
def skill_update(request, pk):
    """Edit an existing skill — only the owner is allowed."""
    skill = get_object_or_404(Skill, pk=pk)

    # Authorization check. We don't use a permission framework here to keep
    # things simple — a plain owner check is enough for a beginner project.
    if skill.owner != request.user:
        return HttpResponseForbidden('You can only edit your own skills.')

    if request.method == 'POST':
        # `instance=skill` tells the form "update this row instead of creating one".
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated.')
            return redirect(skill)
    else:
        form = SkillForm(instance=skill)

    return render(request, 'skills/skill_form.html', {'form': form, 'is_edit': True, 'skill': skill})


@login_required
def skill_delete(request, pk):
    """Confirm + delete a skill — only the owner is allowed."""
    skill = get_object_or_404(Skill, pk=pk)

    if skill.owner != request.user:
        return HttpResponseForbidden('You can only delete your own skills.')

    if request.method == 'POST':
        # Two-step delete: GET shows confirmation, POST actually deletes.
        # This pattern protects against accidental delete-by-link-prefetch.
        skill.delete()
        messages.success(request, 'Skill deleted.')
        return redirect('dashboard')

    return render(request, 'skills/skill_confirm_delete.html', {'skill': skill})


@login_required
def dashboard(request):
    """A user's 'my skills' page — shows ALL of their posts including hidden."""
    my_skills = request.user.skills.all()  # uses related_name='skills'
    return render(request, 'skills/dashboard.html', {'skills': my_skills})
