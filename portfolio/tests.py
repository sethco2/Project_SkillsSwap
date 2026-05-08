from django.test import TestCase
from django.urls import reverse

from .models import Project


class PortfolioPagesTests(TestCase):
    def test_home_renders(self):
        response = self.client.get(reverse("portfolio:home"))
        self.assertEqual(response.status_code, 200)

    def test_projects_index_renders(self):
        response = self.client.get(reverse("portfolio:projects"))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_renders(self):
        project = Project.objects.create(
            title="Test Project",
            one_sentence_summary="A short summary.",
        )
        response = self.client.get(project.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")

    def test_static_pages_render(self):
        for name in ("about", "skills", "resume", "contact"):
            response = self.client.get(reverse(f"portfolio:{name}"))
            self.assertEqual(response.status_code, 200, msg=name)
