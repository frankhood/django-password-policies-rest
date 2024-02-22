from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

User = get_user_model()


class ChangePasswordAPIViewTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.api_client = APIClient()
        self.request_factory = APIRequestFactory()

    def test_post_200(self):
        User.objects.create_user(username="testUser", password="test-test")
        self.api_client.login(username="testUser", password="test-test")
        response = self.api_client.post(
            reverse("password-policies-rest:change-password-api"),
            {
                "new_password1": "Qazxsw1234*",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(PASSWORD_MIN_ENTROPY_SHORT=0.8)
    def _test_post_400_invalid_entropy(self):
        User.objects.create_user(username="testUser", password="test-test")
        self.api_client.login(username="testUser", password="test-test")
        response = self.api_client.post(
            reverse("password-policies-rest:change-password-api"),
            {
                "new_password1": "Iiiii0ooioo0!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_entropy", response.data["non_field_errors"][0])

    @override_settings(PASSWORD_MAX_CONSECUTIVE=3)
    def test_post_400_invalid_consecutive_count(self):
        User.objects.create_user(username="testUser", password="test-test")
        self.api_client.login(username="testUser", password="test-test")
        response = self.api_client.post(
            reverse("password-policies-rest:change-password-api"),
            {
                "new_password1": "Iiiii0ooiioo0!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_consecutive_count", response.data["non_field_errors"][0])
