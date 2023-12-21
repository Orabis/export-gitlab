from unittest.mock import MagicMock, Mock, patch

from django.test import RequestFactory, TestCase
from django.urls import reverse

from exportgitlab.apps.export.models import *
from exportgitlab.apps.export.views import list_all_projects_homepage


class IssuesTest(TestCase):
    def setUp(self):
        self.url = reverse("list_all_issues", kwargs={"id_pj": 1})
        self.user = User.objects.create_user(username="JohnPork", gitlab_token="gyyat1234")
        self.client.force_login(self.user)
        mock_gitlab = patch("exportgitlab.libs.connect.gitlab")
        mock_gitlab.start()
        self.addCleanup(mock_gitlab.stop)

    def test_download_in_group_issues(self):
        url = reverse("download_report_issues", kwargs={"id_pj": 1})
        data = {"grp-ungrp": "group_issue"}
        response = self.client.post(url, data)
