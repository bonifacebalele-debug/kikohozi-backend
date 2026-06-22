"""Tests for clinical-data sync, which depends on a synced participant."""
from rest_framework import status

from apps.mobile.models import ClinicalData
from apps.mobile.tests.helpers import (
    AuthenticatedAPITestCase,
    clinical_data_payload,
    participant_payload,
)

PARTICIPANT_URL = "/api/mobile/sync/participant/"
URL = "/api/mobile/sync/clinical-data/"


class ClinicalDataSyncTests(AuthenticatedAPITestCase):
    def _create_participant(self):
        response = self.client.post(
            PARTICIPANT_URL, participant_payload(), format="json"
        )
        return response.data["server_id"]

    def test_creates_clinical_data_linked_to_participant(self):
        participant_id = self._create_participant()
        payload = clinical_data_payload(participant_id)
        response = self.client.post(URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        record = ClinicalData.objects.get(local_uuid=payload["local_uuid"])
        self.assertEqual(record.participant_id, participant_id)
        self.assertEqual(response.data["server_id"], record.pk)
        self.assertEqual(response.data["participant_server_id"], participant_id)
        # JSON list/dict fields round-trip correctly.
        self.assertEqual(record.laboratory_tests_performed, ["GENEXPERT", "SMEAR"])
        self.assertEqual(record.comorbidity_duration_map, {"DIABETES": {"years": 2}})

    def test_rejects_when_participant_not_yet_synced(self):
        # Ordering enforcement: clinical data cannot reference a missing participant.
        response = self.client.post(
            URL, clinical_data_payload(999999), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["success"])
        self.assertEqual(ClinicalData.objects.count(), 0)

    def test_missing_participant_server_id_is_validation_error(self):
        payload = clinical_data_payload(self._create_participant())
        del payload["participant_server_id"]
        response = self.client.post(URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("participant_server_id", response.data["errors"])

    def test_idempotent_on_duplicate_local_uuid(self):
        participant_id = self._create_participant()
        payload = clinical_data_payload(participant_id)
        first = self.client.post(URL, payload, format="json")
        second = self.client.post(URL, payload, format="json")

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(ClinicalData.objects.count(), 1)
        self.assertEqual(first.data["server_id"], second.data["server_id"])
