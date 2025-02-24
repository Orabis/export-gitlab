from django.test import TestCase
from django.urls import reverse

from exportgitlab.apps.export.models import User


class ProfileTest(TestCase):
    def test_view_anonymous_access_is_not_allowed(self):
        response = self.client.get(reverse("user_profile"))
        self.assertRedirects(response, expected_url="/accounts/login/?next=/profile/", fetch_redirect_response=False)

    def test_view_authenticated_user_can_access(self):
        user = User.objects.create_user(username="John")
        self.client.force_login(user)
        response = self.client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, 200)

    def test_view_anonymous_access_is_not_allowed_on_token_change(self):
        response = self.client.get(reverse("user_change_token"))
        self.assertRedirects(
            response, expected_url="/accounts/login/?next=/profile/token_pending/", fetch_redirect_response=False
        )

    def test_view_authenticated_user_can_access_to_token_change(self):
        user = User.objects.create_user(username="John")
        self.client.force_login(user)
        response = self.client.get(reverse("user_change_token"))
        self.assertEqual(response.status_code, 200)


class TokenRegisterForm(TestCase):
    def setUp(self):
        self.url = reverse("user_change_token")
        self.user = User.objects.create_user(username="John")
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_new_token_invalid_post_data_to_much_character(self):
        data = {
            "gitlab_token": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi maximus auctor lorem, id dictum velit suscipit convallis. Curabitur eget augue eu leo ultrices blandit. Nunc consectetur semper feugiat. Vestibulum pharetra felis eget tellus consectetur gravida. Nullam a consectetur lectus. Vestibulum ante. "
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.user.gitlab_token)

    def test_new_token_valid(self):
        data = {"gitlab_token": "glpat-8LDKS78XytBkBX3SjBUR"}  # example key #
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(data["gitlab_token"], self.user.gitlab_token)
