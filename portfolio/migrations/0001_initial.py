from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("slug", models.SlugField(blank=True, max_length=140, unique=True)),
                ("category", models.CharField(
                    choices=[
                        ("chatbot", "Chatbot"),
                        ("n8n", "n8n Agent Workflow"),
                        ("langchain", "LangChain Agent"),
                        ("ai_studio", "Google AI Studio Media"),
                        ("ml", "Machine Learning (scikit-learn)"),
                        ("django", "Django Web App"),
                        ("other", "Other"),
                    ],
                    default="other",
                    max_length=32,
                )),
                ("one_sentence_summary", models.CharField(max_length=280)),
                ("business_problem", models.TextField(blank=True)),
                ("tools_used", models.TextField(blank=True,
                    help_text="Comma-separated list. Example: Python, LangChain, Google Sheets API")),
                ("key_features", models.TextField(blank=True,
                    help_text="One feature per line. Will render as bullet points.")),
                ("role_contribution", models.TextField(blank=True)),
                ("biggest_challenge", models.TextField(blank=True)),
                ("what_i_learned", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="projects/")),
                ("static_image", models.CharField(blank=True, max_length=200)),
                ("image_alt", models.CharField(blank=True, max_length=200)),
                ("github_link", models.URLField(blank=True)),
                ("demo_link", models.URLField(blank=True)),
                ("featured", models.BooleanField(default=False)),
                ("order", models.PositiveSmallIntegerField(default=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["order", "title"]},
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("group", models.CharField(
                    choices=[
                        ("ai", "AI and Automation"),
                        ("web", "Full-Stack and Web"),
                        ("ml", "Machine Learning and Data"),
                        ("biz", "Business and Creative Strategy"),
                    ],
                    default="ai",
                    max_length=16,
                )),
                ("description", models.CharField(blank=True, max_length=200)),
                ("order", models.PositiveSmallIntegerField(default=100)),
            ],
            options={"ordering": ["group", "order", "name"]},
        ),
        migrations.CreateModel(
            name="PersonalBuild",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("summary", models.CharField(max_length=280)),
                ("url", models.URLField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="personal/")),
                ("order", models.PositiveSmallIntegerField(default=100)),
            ],
            options={"ordering": ["order", "name"]},
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(max_length=120)),
                ("organization", models.CharField(max_length=120)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("start_date", models.CharField(help_text="e.g. 'Aug 2024'", max_length=40)),
                ("end_date", models.CharField(blank=True, help_text="Leave blank for 'Present'", max_length=40)),
                ("description", models.TextField(blank=True, help_text="One bullet per line.")),
                ("order", models.PositiveSmallIntegerField(default=100)),
            ],
            options={"ordering": ["order"]},
        ),
    ]
