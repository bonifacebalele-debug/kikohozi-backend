"""Tests for clinical-medication sync, which depends on a synced clinical-data record."""
from rest_framework import status

from apps.mobile.models import ClinicalData, ClinicalMedication
from apps.mobile.tests.helpers import (
    AuthenticatedAPITestCase,
    clinical_data_payload,
    medications_payload,
    participant_payload,
)

PARTICIPANT_URL = "/api/mobile/sync/participant/"
CLINICAL_URL = "/api/mobile/sync/clinical-data/"
URL = "/api/mobile/sync/clinical-medications/"


class ClinicalMedicationSyncTests(AuthenticatedAPITestCase):
    def _create_clinical_data(self):
        participant_id = self.client.post(
            PARTICIPANT_URL, participant_payload(), format="json"
        ).data["server_id"]
        return self.client.post(
            CLINICAL_URL, clinical_data_payload(participant_id), format="json"
        ).data["server_id"]

    def test_creates_medication_rows(self):
        clinical_id = self._create_clinical_data()
        response = self.client.post(
            URL, medications_payload(clinical_id), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            ClinicalMedication.objects.filter(clinical_data_id=clinical_id).count(), 2
        )

    def test_rejects_when_clinical_data_missing(self):
        response = self.client.post(URL, medications_payload(999999), format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["success"])
        self.assertEqual(ClinicalMedication.objects.count(), 0)

    def test_resync_same_batch_is_idempotent(self):
        clinical_id = self._create_clinical_data()
        payload = medications_payload(clinical_id)
        first = self.client.post(URL, payload, format="json")
        second = self.client.post(URL, payload, format="json")

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        # Idempotency key prevents duplicate rows for the same batch.
        self.assertEqual(
            ClinicalMedication.objects.filter(clinical_data_id=clinical_id).count(), 2
        )

    def test_empty_medications_batch_is_rejected(self):
        clinical_id = self._create_clinical_data()
        response = self.client.post(
            URL, medications_payload(clinical_id, medications=[]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("medications", response.data["errors"])
        self.assertEqual(ClinicalMedication.objects.count(), 0)

    def test_new_batch_replaces_previous_medications(self):
        clinical_id = self._create_clinical_data()
        self.client.post(URL, medications_payload(clinical_id), format="json")

        # A new local_uuid with a single medication should replace the old set.
        replacement = medications_payload(
            clinical_id,
            medications=[
                {
                    "medication_name": "ETHAMBUTOL",
                    "dose_frequency": "OD",
                    "dose_duration": "2_MONTHS",
                    "display_order": 1,
                }
            ],
        )
        response = self.client.post(URL, replacement, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        meds = ClinicalMedication.objects.filter(clinical_data_id=clinical_id)
        self.assertEqual(meds.count(), 1)
        self.assertEqual(meds.first().medication_name, "ETHAMBUTOL")

        clinical = ClinicalData.objects.get(pk=clinical_id)
        self.assertEqual(clinical.medications_local_uuid, replacement["local_uuid"])
