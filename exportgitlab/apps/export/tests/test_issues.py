from unittest.mock import MagicMock, Mock, patch

from django.test import RequestFactory, TestCase
from django.urls import reverse

from exportgitlab.apps.export.models import *
from exportgitlab.apps.export.views import (
    list_all_issues,
    list_all_projects_homepage,
)

# class IssuesTest(TestCase):
#    def setUp(self):
#        self.project = Project.objects.create(gitlab_id="12345", name="TestPj", description=None, url="TestPj/")
#        self.url = reverse("list_all_issues", kwargs={"id_pj": self.project.id})
#        self.user = User.objects.create_user(username="JohnPork", gitlab_token="gyyat1234")
#        self.client.force_login(self.user)
#        mock_gitlab = patch("exportgitlab.libs.gitlab.gitlab")
#        mock_gitlab.start()
#        self.addCleanup(mock_gitlab.stop)
#
#
# def test_valid_parameter_filter_issues(self):
#     with patch("exportgitlab.libs.gitlab.gitlab.Gitlab") as gl_mock:
#         project_mock = gl_mock().projects.get.return_value
#         project_mock.gitlab_id = 1
#         label1 = Mock()
#         label2 = Mock()
#         label1.configure_mock(name="labeltest1", color="red")
#         label2.configure_mock(name="labeltest2", color="yellow")
#         project_mock.labels.list.return_value = [label1, label2]
#         project_mock.issues.list.return_value = []
#         request = RequestFactory().get(
#             self.url, data={"iid": "123", "lab": ["labeltest1", "labeltest2"], "oc": "open"}
#         )
#         request.user = self.user
#         request.gl = gl_mock
#         response = list_all_issues(request, self.project.id)
#         self.assertEqual()
