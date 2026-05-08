from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import Experience, PersonalBuild, Project, Skill


def home(request):
    featured = Project.objects.filter(featured=True)[:3]
    if not featured.exists():
        featured = Project.objects.all()[:3]
    builds = PersonalBuild.objects.all()[:5]
    return render(request, "portfolio/home.html", {
        "featured_projects": featured,
        "personal_builds": builds,
    })


def about(request):
    return render(request, "portfolio/about.html")


def projects_index(request):
    projects = Project.objects.all()
    builds = PersonalBuild.objects.all()
    return render(request, "portfolio/projects_index.html", {
        "projects": projects,
        "personal_builds": builds,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "portfolio/project_detail.html", {"project": project})


def skills(request):
    grouped = []
    for value, label in Skill.Group.choices:
        items = Skill.objects.filter(group=value)
        if items.exists():
            grouped.append((label, items))
    return render(request, "portfolio/skills.html", {"grouped": grouped})


def resume(request):
    experiences = Experience.objects.all()
    return render(request, "portfolio/resume.html", {"experiences": experiences})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Honeypot — silently drop bot submissions.
        if form.cleaned_data.get("website"):
            return redirect("portfolio:contact")

        contact_to = getattr(settings, "CONTACT_EMAIL", "")
        try:
            if contact_to:
                send_mail(
                    subject=f"[Portfolio] {form.cleaned_data.get('subject') or 'New message'}",
                    message=(
                        f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                        f"{form.cleaned_data['message']}"
                    ),
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", contact_to),
                    recipient_list=[contact_to],
                    fail_silently=False,
                )
                messages.success(request, "Thanks — your message was sent.")
            else:
                messages.info(
                    request,
                    "SMTP isn't configured yet. Use the email link below or "
                    "add EMAIL_* env vars to enable the form.",
                )
        except Exception:
            messages.warning(
                request,
                "Couldn't send right now. Please email me directly using the link below.",
            )
        return redirect("portfolio:contact")

    return render(request, "portfolio/contact.html", {"form": form})
