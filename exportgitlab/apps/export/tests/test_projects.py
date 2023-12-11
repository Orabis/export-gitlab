from django.test import TestCase
from django.urls import reverse

from exportgitlab.apps.export.models import *


class ProjectsTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(gitlab_id="12345", name="TestPj", description=None, url="TestPj/")
        self.user = User.objects.create_user(username="John", gitlab_token=None)

    def test_homepage_is_returning_to_projects_urls(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_projects_redirect_to_profile_if_user_got_no_gitlab_token(self):
        self.client.force_login(self.user)
        self.project.refresh_from_db()
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 302)

    def test_projects_view_authenticated_and_gitlab_token_registered(self):
        user = User.objects.create_user(username="JohnPork", gitlab_token="gyyat1234")
        self.client.force_login(user)
        self.project.refresh_from_db()
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 200)

    def test_successful_redirect_to_projects(self):
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 302)


class ProjectRegisterForm(TestCase):
    ...

    # def test_projects_view_authenticated_and_gitlab_token_registered(self):
    #   user = User.objects.create_user(username="JohnPork", gitlab_token="gyyat1234")
    #   self.client.force_login(user)
    #   response = self.client.get(reverse("projects"))
    #   self.assertEqual(response.status_code, 200)
