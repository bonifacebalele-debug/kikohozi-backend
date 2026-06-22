"""Tests for participant synchronization — the root of the sync dependency chain."""
from unittest import mock

from django.db import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase

from apps.mobile.models import Participant
from apps.mobile.tests.helpers import (
    AuthenticatedAPITestCase,
    participant_payload,
)

URL = "/api/mobile/sync/participant/"


class ParticipantSyncAuthTests(APITestCase):
    def test_requires_authentication(self):
        response = self.client.post(URL, participant_payload(), format="json")
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )


class ParticipantSyncTests(AuthenticatedAPITestCase):
    def test_creates_participant_and_returns_server_id(self):
        payload = participant_payload()
        response = self.client.post(URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])

        participant = Participant.objects.get(local_uuid=payload["local_uuid"])
        self.assertEqual(response.data["server_id"], participant.pk)
        self.assertEqual(response.data["server_participant_id"], participant.pk)
        # synced_by is attributed to the authenticated user.
        self.assertEqual(participant.synced_by, self.user)

    def test_generates_human_readable_participant_id(self):
        response = self.client.post(URL, participant_payload(), format="json")
        generated = response.data["generated_participant_id"]
        self.assertTrue(generated.startswith("KIK-MUHA-2026-"))
        # Nested data block carries the same id (redundant keys for the parser).
        self.assertEqual(
            response.data["data"]["participant"]["generated_participant_id"], generated
        )

    def test_idempotent_on_duplicate_local_uuid(self):
        payload = participant_payload()
        first = self.client.post(URL, payload, format="json")
        second = self.client.post(URL, payload, format="json")

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        # Re-sending the same draft must not create a second row.
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(Participant.objects.count(), 1)
        self.assertEqual(first.data["server_id"], second.data["server_id"])

    def test_concurrent_duplicate_recovers_without_500(self):
        # First request genuinely creates the participant.
        payload = participant_payload()
        self.client.post(URL, payload, format="json")
        existing = Participant.objects.get(local_uuid=payload["local_uuid"])

        # Simulate a true race: the pre-check misses the row, create() then loses the
        # unique-constraint race, and the view must recover by returning the winner
        # instead of bubbling a 500 up to the device.
        with mock.patch("apps.mobile.views.sync.Participant") as MockParticipant:
            MockParticipant.objects.filter.return_value.first.side_effect = [None, existing]
            MockParticipant.objects.create.side_effect = IntegrityError("duplicate local_uuid")
            response = self.client.post(URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["server_id"], existing.pk)
        self.assertEqual(Participant.objects.count(), 1)

    def test_validation_error_returns_400_with_errors(self):
        payload = participant_payload()
        del payload["site_code"]  # required field
        response = self.client.post(URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("site_code", response.data["errors"])
        self.assertEqual(Participant.objects.count(), 0)

    def test_invalid_date_is_rejected(self):
        response = self.client.post(
            URL, participant_payload(date_of_recruitment="not-a-date"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date_of_recruitment", response.data["errors"])
