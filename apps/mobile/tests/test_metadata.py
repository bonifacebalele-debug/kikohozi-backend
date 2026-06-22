"""Tests for the metadata endpoint that drives the app's dropdowns."""
from rest_framework import status
from rest_framework.test import APITestCase

from apps.mobile.tests.helpers import AuthenticatedAPITestCase


class MetadataAuthTests(APITestCase):
    def test_metadata_requires_authentication(self):
        response = self.client.get("/api/mobile/metadata/")
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )


class MetadataContentTests(AuthenticatedAPITestCase):
    def test_metadata_returns_all_top_level_sections(self):
        response = self.client.get("/api/mobile/metadata/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        data = response.data["data"]
        for section in (
            "participant",
            "clinical_data",
            "clinical_medication",
            "cough_recording",
        ):
            self.assertIn(section, data, f"metadata missing section: {section}")

    def test_participant_metadata_has_region_to_districts(self):
        response = self.client.get("/api/mobile/metadata/")
        participant = response.data["data"]["participant"]
        self.assertIn("region_choices", participant)
        self.assertIn("region_to_districts", participant)
        self.assertIsInstance(participant["region_to_districts"], dict)
