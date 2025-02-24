import json
from http import HTTPStatus

import responses
from django.test import TestCase
from django.urls import reverse

from exportgitlab.apps.export.models import Project, User
#MODIFY THE FILE DATA FOR TESTING GITLAB USER API
with open("exportgitlab/apps/export/tests/fixtures/user_request.json") as f:
    user_json = json.load(f)

with open("exportgitlab/apps/export/tests/fixtures/project_request.json") as f:
    project_json = json.load(f)

with open("exportgitlab/apps/export/tests/fixtures/labels_request.json") as f:
    labels_json = json.load(f)

with open("exportgitlab/apps/export/tests/fixtures/issues_request.json") as f:
    issues_json = json.load(f)


def get_profile_response() -> responses.Response:
    response = responses.Response(
        method=responses.GET,
        url="https://gitlab.com/api/v4/user",
        json=user_json,
    )
    return response


class IssuesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="John", gitlab_token="gyyat1234")
        self.project = Project.objects.create(gitlab_id="34755", name="TestPj", description=None, url="TestPj/")
        self.client.force_login(self.user)
        responses.add(get_profile_response())
        responses.add(
            responses.GET,
            "https://gitlab.com/api/v4/projects/34755",
            json=project_json,
        )
        responses.add(responses.GET, "https://gitlab.com/api/v4/projects/67410665/labels", json=labels_json)
        responses.add(responses.GET, "https://gitlab.com/api/v4/projects/67410665/issues?labels=", json=issues_json)
        responses.add(responses.GET, "https://gitlab.com/api/v4/projects/67410665/issues", json=issues_json)

    @responses.activate
    def test_api_issues(self):
        response = self.client.get(reverse("issues_info", kwargs={"id_pj": self.project.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(issues_json[0]["title"], response.content.decode("utf-8"))

    @responses.activate
    def test_api_labels(self):
        response = self.client.get(reverse("labels_info", kwargs={"id_pj": self.project.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(labels_json[0]["name"], response.content.decode("utf-8"))

    @responses.activate
    def test_api_project(self):
        response = self.client.get(reverse("project_info", kwargs={"id_pj": self.project.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(str(project_json["id"]), response.content.decode("utf-8"))
