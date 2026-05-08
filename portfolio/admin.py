from django.contrib import admin

from .models import Experience, PersonalBuild, Project, Skill


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "order", "updated_at")
    list_editable = ("featured", "order")
    list_filter = ("category", "featured")
    search_fields = ("title", "one_sentence_summary", "tools_used")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Overview", {
            "fields": ("title", "slug", "category", "one_sentence_summary",
                       "featured", "order"),
        }),
        ("Case study (rubric sections 3-8)", {
            "fields": ("business_problem", "tools_used", "key_features",
                       "role_contribution", "biggest_challenge",
                       "what_i_learned"),
        }),
        ("Visual & links (rubric sections 9-10)", {
            "fields": ("image", "static_image", "image_alt",
                       "github_link", "demo_link"),
            "description": "Use 'image' to upload, or 'static_image' for a "
                           "path inside /static/ (e.g. media/handyman.png).",
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "order")
    list_editable = ("group", "order")
    list_filter = ("group",)
    search_fields = ("name", "description")


@admin.register(PersonalBuild)
class PersonalBuildAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order")
    list_editable = ("order",)
    search_fields = ("name", "summary")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organization", "start_date", "end_date", "order")
    list_editable = ("order",)
    search_fields = ("role", "organization")
