"""
Register the Skill model with Django's admin site so superusers can
view, search, filter, and edit posts at /admin/.

Customizing ModelAdmin is optional but a tiny bit of polish goes a
long way for usability.
"""
from django.contrib import admin
from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    # Columns shown on the change-list page
    list_display = ('title', 'owner', 'category', 'display_price',
                    'is_available', 'created_at')

    # Right-hand sidebar filters
    list_filter  = ('category', 'is_available', 'is_free', 'created_at')

    # Top-of-page search box (searches these fields)
    search_fields = ('title', 'description', 'owner__username')

    # Make created_at read-only since it's auto-set
    readonly_fields = ('created_at',)
