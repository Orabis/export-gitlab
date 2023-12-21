from unittest.mock import Mock, patch

from django.test import TestCase

from exportgitlab.libs.connect import gl_connection


class GitlabConnectTest(TestCase):
    def test_gitlab_successful_connection(self):
        with patch("exportgitlab.libs.connect.gitlab") as mock_gitlab:
            mock_gl = Mock()
            mock_gitlab.Gitlab.return_value = mock_gl
            connection_return = gl_connection("test1234")
            self.assertIs(connection_return, mock_gl)

        mock_gitlab.Gitlab.assert_called_with(url="https://git.unistra.fr", private_token="test1234")
        mock_gitlab.auth.called_once()

    def test_gitlab_connection_error(self):
        ...
