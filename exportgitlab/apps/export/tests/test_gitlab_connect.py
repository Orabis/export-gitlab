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

        mock_gitlab.Gitlab.assert_called_with(url="https://gitlab.com/", private_token="test1234")
        mock_gl.auth.assert_called_once()

    def test_gitlab_get_labels(self):
        with patch("exportgitlab.libs.gitlab.gitlab.Gitlab") as gl_mock:
            gitlab_project = gl_mock().projects.get.return_value
            label1 = Mock()
            label2 = Mock()
            label1.configure_mock(name="labeltest1", color="#dc143c", id="1")
            label2.configure_mock(name="labeltest2", color="#330066", id="2")
            gitlab_project.labels.list.return_value = [label1, label2]
            expected_array = [
                {"name": "labeltest1", "bg_color": "#dc143c", "text_color": "#FFFFF", "id": "1"},
                {"name": "labeltest2", "bg_color": "#330066", "text_color": "#FFFFF", "id": "2"},
            ]
            self.assertEqual(expected_array, get_labels_list(gitlab_project))

    def test_gitlab_get_all_issues(self):
        with patch("exportgitlab.libs.gitlab.gitlab") as gl_mock:
            gitlab_project = gl_mock().projects.get.return_value
            get_issues(gitlab_project)
            gitlab_project.issues.list.assert_called_with(get_all=True)
