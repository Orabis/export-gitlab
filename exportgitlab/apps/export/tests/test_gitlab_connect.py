from unittest.mock import Mock, patch

from django.test import TestCase

from exportgitlab.libs.gitlab import get_issues, get_labels_list, gl_connection


class GitlabConnectTest(TestCase):
    def test_gitlab_successful_connection(self):
        with patch("exportgitlab.libs.gitlab.gitlab") as mock_gitlab:
            mock_gl = Mock()
            mock_gitlab.Gitlab.return_value = mock_gl
            connection_return = gl_connection("test1234")
            self.assertIs(connection_return, mock_gl)

        mock_gitlab.Gitlab.assert_called_with(url="https://git.unistra.fr", private_token="test1234")
        mock_gitlab.auth.called_once()

    def test_gitlab_get_labels(self):
        with patch("exportgitlab.libs.gitlab.gitlab.Gitlab") as gl_mock:
            gitlab_project = gl_mock().projects.get.return_value
            label1 = Mock()
            label2 = Mock()
            label1.configure_mock(name="labeltest1", color="#dc143c")
            label2.configure_mock(name="labeltest2", color="#330066")
            gitlab_project.labels.list.return_value = [label1, label2]
            expected_dict = {
                "labeltest1": {"bg_color": "#dc143c", "text_color": "#FFFFF"},
                "labeltest2": {"bg_color": "#330066", "text_color": "#FFFFF"},
            }
            self.assertEqual(expected_dict, get_labels_list(gitlab_project))

    def test_gitlab_get_issues_with_no_id_and_labels(self):
        with patch("exportgitlab.libs.gitlab.gitlab") as gl_mock:
            gitlab_project = gl_mock().projects.get.return_value
            opened_closed_filter = "opened"
            iid_filter = [""]
            labels_filter = ["label1", "label2"]
            get_issues(gitlab_project, iid_filter, labels_filter, opened_closed_filter)
            gitlab_project.issues.list.assert_called_with(
                get_all=True, state=opened_closed_filter, labels=labels_filter
            )

    def test_gitlab_get_issues_with_id_and_no_labels(self):
        with patch("exportgitlab.libs.gitlab.gitlab") as gl_mock:
            gitlab_project = gl_mock().projects.get.return_value
            opened_closed_filter = "opened"
            iid_filter = ["130,127"]
            labels_filter = [""]
            get_issues(gitlab_project, iid_filter, labels_filter, opened_closed_filter)
            gitlab_project.issues.list.assert_called_with(get_all=True, state=opened_closed_filter, iids=iid_filter)

    def test_gitlab_get_issues_with_no_id_and_no_labels(self):
        with patch("exportgitlab.libs.gitlab.gitlab") as gl_mock:
            gitlab_project = gl_mock().projects.get.return_value
            opened_closed_filter = "opened"
            iid_filter = [""]
            labels_filter = [""]
            get_issues(gitlab_project, iid_filter, labels_filter, opened_closed_filter)
            gitlab_project.issues.list.assert_called_with(get_all=True, state=opened_closed_filter)

    def test_gitlab_get_issues_with_id_and_labels(self):
        with patch("exportgitlab.libs.gitlab.gitlab") as gl_mock:
            gitlab_project = gl_mock().projects.get.return_value
            opened_closed_filter = "opened"
            iid_filter = ["130,127"]
            labels_filter = ["label1", "label2"]
            get_issues(gitlab_project, iid_filter, labels_filter, opened_closed_filter)
            gitlab_project.issues.list.assert_called_with(
                get_all=True, state=opened_closed_filter, iids=iid_filter, labels=labels_filter
            )
