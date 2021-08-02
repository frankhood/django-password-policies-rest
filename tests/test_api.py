from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from password_policies.conf import settings as password_settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

User = get_user_model()


class ChangePasswordAPIViewTest(APITestCase):

    def setUp(self):
        super().setUp()
        self.api_client = APIClient()
        self.request_factory = APIRequestFactory()

    def test_post_200(self):
        User.objects.create_user(username="testUser", password="test-test")
        self.api_client.login(username='testUser', password='test-test')
        response = self.api_client.post(
            reverse("password-policies-rest:change-password-api"),
            {
                "new_password1": "Qazxsw1234*",
            },
            format='json'
        )
        print("response : %s" % response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(PASSWORD_MIN_ENTROPY_SHORT=0.8)
    def test_post_400_invalid_entropy(self):
        User.objects.create_user(username="testUser", password="test-test")
        self.api_client.login(username='testUser', password='test-test')
        print(password_settings.PASSWORD_MIN_ENTROPY_SHORT)
        response = self.api_client.post(
            reverse("password-policies-rest:change-password-api"),
            {
                "new_password1": "Iiiii0ooioo0!",
            },
            format='json'
        )
        # print("Response : %s" % response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_entropy", response.data['non_field_errors'][0])

    @override_settings(PASSWORD_MAX_CONSECUTIVE=3)
    def test_post_400_invalid_consecutive_count(self):
        User.objects.create_user(username="testUser", password="test-test")
        self.api_client.login(username='testUser', password='test-test')
        response = self.api_client.post(
            reverse("password-policies-rest:change-password-api"),
            {
                "new_password1": "Iiiii0ooiioo0!",
            },
            format='json'
        )
        print("Response : %s" % response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_consecutive_count", response.data['non_field_errors'][0])

    @override_settings(PASSWORD_MIN_UPPERCASE_LETTERS=1)
    def test_post_400(self):
        User.objects.create_user(username="testUser", password="test-test")

        self.api_client.login(username='testUser', password='test-test')
        with self.subTest("invalid_uppercaseletter_count"):
            print("password_settings.PASSWORD_MIN_UPPERCASE_LETTERS : {}".format(password_settings.PASSWORD_MIN_UPPERCASE_LETTERS))
            response = self.api_client.post(
                reverse("password-policies-rest:change-password-api"),
                {
                    "new_password1": "qazxsw1234*",
                },
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("invalid_uppercaseletter_count", response.data['non_field_errors'][0])

        # see password_policies.tests.test_forms for other tests
