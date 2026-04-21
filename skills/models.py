"""
Database models for the Skills app.

A "model" is a Python class that maps to a single database table. Each
attribute on the class becomes a column. Django reads this file, generates
SQL via `makemigrations`, and applies it via `migrate`.
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Skill(models.Model):
    """A single skill or service a student is offering."""

    # --- Choices --------------------------------------------------------
    # Defining choices as tuples gives us a dropdown in forms/admin and
    # validates that nobody sneaks in an unexpected value.
    CATEGORY_CHOICES = [
        ('tutoring',    'Tutoring'),
        ('design',      'Design & Creative'),
        ('coding',      'Coding & Tech'),
        ('writing',     'Writing & Editing'),
        ('music',       'Music Lessons'),
        ('fitness',     'Fitness & Wellness'),
        ('moving',      'Moving & Errands'),
        ('other',       'Other'),
    ]

    CONTACT_CHOICES = [
        ('email',    'Email'),
        ('phone',    'Phone / Text'),
        ('discord',  'Discord'),
        ('inperson', 'In Person'),
    ]

    # --- Fields ---------------------------------------------------------
    title = models.CharField(
        max_length=120,
        help_text='Short headline e.g. "Calculus tutoring for first-years"',
    )

    description = models.TextField(
        help_text='Longer explanation of what you offer, your experience, etc.',
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
    )

    # Price stored as DecimalField (NOT FloatField — money + floats = bugs).
    # `null=True, blank=True` means the field can be left empty, which we
    # use together with `is_free` so users can post a free service.
    price = models.DecimalField(
        max_digits=6,            # up to 9999.99
        decimal_places=2,
        null=True, blank=True,
        help_text='Leave blank if this is a free service.',
    )
    is_free = models.BooleanField(
        default=False,
        help_text='Tick if you offer this for free.',
    )

    contact_preference = models.CharField(
        max_length=20,
        choices=CONTACT_CHOICES,
        default='email',
    )

    is_available = models.BooleanField(
        default=True,
        help_text='Untick to temporarily hide this skill from the public list.',
    )

    # auto_now_add stamps the creation time once and never changes it.
    created_at = models.DateTimeField(auto_now_add=True)

    # ForeignKey = "many skills belong to one user".
    # on_delete=CASCADE: if the user is deleted, their skills go with them.
    # related_name='skills' lets us write `request.user.skills.all()`.
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='skills',
    )

    # --- Meta options ---------------------------------------------------
    class Meta:
        # Newest skills first when we query Skill.objects.all()
        ordering = ['-created_at']

    # --- Python-level helpers ------------------------------------------
    def __str__(self):
        # Shown in the admin and anywhere a Skill is converted to text.
        return self.title

    def get_absolute_url(self):
        # Lets Django (and our templates) figure out the canonical URL of
        # a skill via `skill.get_absolute_url`. Used after create/update.
        return reverse('skill_detail', args=[self.pk])

    def display_price(self):
        """Friendly string for templates: 'Free' or '$25.00'."""
        if self.is_free or self.price is None:
            return 'Free'
        return f'${self.price:.2f}'
