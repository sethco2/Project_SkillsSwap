"""
Portfolio app models.

Designed so the entire portfolio (project case studies, skills, personal
builds, experience) is editable from Django admin without touching code.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Project(models.Model):
    """A class project case study, rendered on the project detail page.

    Fields map 1:1 to the rubric's required 10 sections so admins can
    paste content in without thinking about template structure.
    """

    class Category(models.TextChoices):
        CHATBOT = "chatbot", "Chatbot"
        N8N = "n8n", "n8n Agent Workflow"
        LANGCHAIN = "langchain", "LangChain Agent"
        AI_STUDIO = "ai_studio", "Google AI Studio Media"
        ML = "ml", "Machine Learning (scikit-learn)"
        DJANGO = "django", "Django Web App"
        OTHER = "other", "Other"

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    category = models.CharField(
        max_length=32, choices=Category.choices, default=Category.OTHER
    )

    # Rubric: required 10 sections
    one_sentence_summary = models.CharField(max_length=280)
    business_problem = models.TextField(blank=True)
    tools_used = models.TextField(
        blank=True,
        help_text="Comma-separated list. Example: Python, LangChain, Google Sheets API",
    )
    key_features = models.TextField(
        blank=True,
        help_text="One feature per line. Will render as bullet points.",
    )
    role_contribution = models.TextField(blank=True)
    biggest_challenge = models.TextField(blank=True)
    what_i_learned = models.TextField(blank=True)

    # Visual + links (item 9 + 10 of the rubric)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    # Fallback path inside /static/ used when there's no uploaded image —
    # lets seed migrations ship visuals out of the box. Example:
    # "media/handyman-terminal.png" → resolved by the template via {% static %}.
    static_image = models.CharField(max_length=200, blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    github_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True)

    # Display controls
    featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:140]
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    @property
    def tools_list(self) -> list[str]:
        return [t.strip() for t in self.tools_used.split(",") if t.strip()]

    @property
    def features_list(self) -> list[str]:
        return [
            line.strip().lstrip("-•").strip()
            for line in self.key_features.splitlines()
            if line.strip()
        ]


class Skill(models.Model):
    """A skill bullet shown on the Skills page, grouped by category."""

    class Group(models.TextChoices):
        AI = "ai", "AI and Automation"
        WEB = "web", "Full-Stack and Web"
        ML = "ml", "Machine Learning and Data"
        BIZ = "biz", "Business and Creative Strategy"

    name = models.CharField(max_length=80)
    group = models.CharField(max_length=16, choices=Group.choices, default=Group.AI)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ["group", "order", "name"]

    def __str__(self) -> str:
        return self.name


class PersonalBuild(models.Model):
    """Beyond-the-classroom work: ventures, sites, automation systems."""

    name = models.CharField(max_length=120)
    summary = models.CharField(max_length=280)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to="personal/", blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class Experience(models.Model):
    """Optional resume-style entries shown on the Resume page."""

    role = models.CharField(max_length=120)
    organization = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.CharField(max_length=40, help_text="e.g. 'Aug 2024'")
    end_date = models.CharField(
        max_length=40, blank=True, help_text="Leave blank for 'Present'"
    )
    description = models.TextField(blank=True, help_text="One bullet per line.")
    order = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.role} — {self.organization}"

    @property
    def bullets(self) -> list[str]:
        return [
            line.strip().lstrip("-•").strip()
            for line in self.description.splitlines()
            if line.strip()
        ]
