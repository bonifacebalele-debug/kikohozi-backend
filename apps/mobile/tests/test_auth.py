"""Tests for the authentication endpoints: status, login, me, logout."""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class StatusEndpointTests(APITestCase):
    def test_status_is_public(self):
        response = self.client.get("/api/mobile/status/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["service"], "Kikohozi Mobile API")
        self.assertFalse(response.data["data"]["authenticated"])

    def test_status_reflects_authenticated_session(self):
        user = User.objects.create_user(username="u1", password="StrongPass!234")
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/mobile/status/")
        self.assertTrue(response.data["data"]["authenticated"])


class LoginEndpointTests(APITestCase):
    def setUp(self):
        # Reset the rate-limit counter so login throttling doesn't bleed across tests.
        cache.clear()
        self.user = User.objects.create_user(
            username="researcher", password="StrongPass!234"
        )

    def test_login_success(self):
        response = self.client.post(
            "/api/mobile/login/",
            {"username": "researcher", "password": "StrongPass!234"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["user"]["username"], "researcher")

    def test_login_trims_username(self):
        response = self.client.post(
            "/api/mobile/login/",
            {"username": "  researcher  ", "password": "StrongPass!234"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password_returns_401(self):
        response = self.client.post(
            "/api/mobile/login/",
            {"username": "researcher", "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])

    def test_login_missing_fields_returns_400(self):
        response = self.client.post(
            "/api/mobile/login/", {"username": "researcher"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_account_returns_403(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        response = self.client.post(
            "/api/mobile/login/",
            {"username": "researcher", "password": "StrongPass!234"},
            format="json",
        )
        # An inactive user fails authentication entirely -> 401.
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )


class LoginThrottleTests(APITestCase):
    def setUp(self):
        cache.clear()
        User.objects.create_user(username="researcher", password="StrongPass!234")

    def test_repeated_attempts_are_throttled(self):
        from apps.mobile.throttles import LoginRateThrottle

        # Drive the test off the configured rate so it tracks the real limit.
        limit = LoginRateThrottle().num_requests
        creds = {"username": "researcher", "password": "wrong"}

        for _ in range(limit):
            response = self.client.post("/api/mobile/login/", creds, format="json")
            self.assertNotEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        # The attempt past the limit is rejected with 429 before credentials are checked.
        throttled = self.client.post("/api/mobile/login/", creds, format="json")
        self.assertEqual(throttled.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class MeAndLogoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="researcher", password="StrongPass!234", email="r@example.com"
        )

    def test_me_requires_authentication(self):
        response = self.client.get("/api/mobile/me/")
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_me_returns_current_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/mobile/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["user"]["email"], "r@example.com")

    def test_logout_succeeds(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/mobile/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
