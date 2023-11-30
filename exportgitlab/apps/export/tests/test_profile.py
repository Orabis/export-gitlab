from django.test import TestCase
from django.urls import reverse
from exportgitlab.apps.export.models import User


class ProfileTest(TestCase):
    def test_view_anonymous_access_is_not_allowed(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, expected_url="/cas/login?next=%2Fprofile%2F", fetch_redirect_response=False)

    def test_view_authenticated_user_can_access(self):
        user = User.objects.create_user(username="John")
        self.client.force_login(user)
        response = self.client.get(reverse("profile"))
        self.assertEquals(response.status_code, 200)

    def test_view_anonymous_access_is_not_allowed_on_token_change(self):
        response = self.client.get(reverse("tokenchangedpending"))
        self.assertRedirects(
            response, expected_url="/cas/login?next=/profile/token_pending/", fetch_redirect_response=False
        )

    def test_view_authenticated_user_can_access_to_token_change(self):
        user = User.objects.create_user(username="John")
        self.client.force_login(user)
        response = self.client.get(reverse("tokenchangedpending"))
        self.assertEquals(response.status_code, 200)


class TokenRegisterForm(TestCase):
    def setUp(self):
        url = reverse("tokenchangedpending")
        self.user = User.objects.create_user(username="John")
        self.client.force_login(self.user)
        self.response = self.client.get(url)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_new_topic_invalid_post_data_to_much_character(self):
        url = reverse("tokenchangedpending")
        data = {
            "gitlab_token": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi maximus auctor lorem, id dictum velit suscipit convallis. Curabitur eget augue eu leo ultrices blandit. Nunc consectetur semper feugiat. Vestibulum pharetra felis eget tellus consectetur gravida. Nullam a consectetur lectus. Vestibulum ante. "
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertIsNone(self.user.gitlab_token)
