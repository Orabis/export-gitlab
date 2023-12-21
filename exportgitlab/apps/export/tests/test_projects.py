from unittest.mock import MagicMock, Mock, patch

from django.contrib import messages
from django.test import RequestFactory, TestCase
from django.urls import reverse
from gitlab import GitlabGetError

from exportgitlab.apps.export.models import *
from exportgitlab.apps.export.views import list_all_projects_homepage


class ProjectsTest(TestCase):
    def setUp(self):
        self.url = reverse("list_all_projects_homepage")
        self.project = Project.objects.create(gitlab_id="12345", name="TestPj", description=None, url="TestPj/")
        self.user = User.objects.create_user(username="JohnPork", gitlab_token="gyyat1234")
        mock_gitlab = patch("exportgitlab.libs.connect.gitlab")
        mock_gitlab.start()
        self.addCleanup(mock_gitlab.stop)

    def test_homepage_is_returning_to_projects_urls(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_projects_redirect_to_profile_if_user_got_no_gitlab_token(self):
        user = User.objects.create_user(username="John", gitlab_token=None)
        self.project.refresh_from_db()
        response = self.client.get(reverse("list_all_projects_homepage"))
        self.assertEqual(response.status_code, 302)

    def test_projects_view_authenticated_and_gitlab_token_registered(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("list_all_projects_homepage"))
        self.assertEqual(response.status_code, 200)

    def test_successful_redirect_to_projects(self):
        response = self.client.get(reverse("list_all_projects_homepage"))
        self.assertEqual(response.status_code, 302)

    def test_project_filter_name_return_when_exist(self):
        data = {"project_name_filter": "TestPj"}
        self.client.force_login(self.user)
        response = self.client.get(self.url, data)
        project_context = response.context["page_obj"]
        self.assertEqual(project_context.object_list.pop(), self.project)
        self.assertEqual(response.status_code, 200)

    def test_create_project(self):
        with patch("exportgitlab.libs.connect.gitlab.Gitlab") as gl_mock:
            project_mock = gl_mock().projects.get.return_value
            project_mock.name_with_namespace = "Testgyat"
            project_mock.web_url = "https://example.com"
            project_mock.description = "Test description"
            request = RequestFactory().post(reverse("list_all_projects_homepage"), data={"gitlab_id": 1})
            request._messages = messages.storage.default_storage(request)
            request.user = self.user
            request.gl = gl_mock
            response = list_all_projects_homepage(request)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                project_mock.name_with_namespace, Project.objects.get(name=project_mock.name_with_namespace).name
            )

    def test_create_project_error(self):
        with patch("exportgitlab.libs.connect.gitlab.Gitlab") as gl_mock:
            gl_mock().projects.get.side_effect = GitlabGetError(response_code=404)
            request = RequestFactory().post(reverse("list_all_projects_homepage"), data={"gitlab_id": 1})
            request._messages = messages.storage.default_storage(request)
            request.user = self.user
            request.gl = gl_mock
            response = list_all_projects_homepage(request)
            error_message = [m.message for m in request._messages][0]
            self.assertEqual("Le Project n'existe pas", error_message)
            self.assertEqual(response.status_code, 200)

    # def test_refresh_project_(self):
    #    with patch("exportgitlab.libs.connect.gitlab.Gitlab") as gl_mock:
    #        project_mock = gl_mock().projects.get.return_value
    #        project_mock.name_with_namespace = "Testgyat"
