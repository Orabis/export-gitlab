import json

import responses
from django.test import TestCase
from django.urls import reverse

from exportgitlab.apps.export.models import Project, User
#MODIFY THE FILE DATA FOR TESTING GITLAB USER API
with open("exportgitlab/apps/export/tests/fixtures/user_request.json") as f:
    user_json = json.load(f)

with open("exportgitlab/apps/export/tests/fixtures/project_request.json") as f:
    project_json = json.load(f)

with open("exportgitlab/apps/export/tests/fixtures/issue_request.json") as f:
    issue_json = json.load(f)

with open("exportgitlab/apps/export/tests/fixtures/simple-image.jpg", "rb") as f:
    image_png = f.read()

with open("exportgitlab/apps/export/tests/fixtures/pdf_request_file.pdf", "rb") as f:
    request_pdf = f.read()


def get_profile_response() -> responses.Response:
    response = responses.Response(
        method=responses.GET,
        url="https://gitlab.com/api/v4/user",
        json=user_json,
    )
    return response


def responses_add():
    responses.add(get_profile_response())
    responses.add(responses.GET, "https://gitlab.com/api/v4/projects/34755", json=project_json)
    responses.add(responses.GET, "https://gitlab.com/api/v4/projects/34755/issues/1", json=issue_json)
    responses.add(responses.POST, "http://localhost:8001", body=request_pdf)


class IssuesReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="John", gitlab_token="gyyat1234")
        self.project = Project.objects.create(gitlab_id="34755", name="TestPj", description=None, url="TestPj/")

    @responses.activate
    def test_download_group_issues(self):
        responses_add()

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("download_report_issues", kwargs={"id_pj": self.project.id}),
            data={"checkbox_issues": 1, "grp-ungrp": "group_issue"},
        )
        self.assertIn("application/pdf", str(response.headers))

    @responses.activate
    def test_download_ungroup_issues(self):
        responses_add()

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("download_report_issues", kwargs={"id_pj": self.project.id}),
            data={"checkbox_issues": 1, "grp-ungrp": "ungroup_issue"},
        )
        self.assertIn("application/zip", str(response.headers))

    @responses.activate
    def test_download_error(self):
        responses_add()
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("download_report_issues", kwargs={"id_pj": self.project.id}), data={"checkbox_issues": 1}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(response.wsgi_request._messages._queued_messages[0]), "Erreur de téléchargement ")
