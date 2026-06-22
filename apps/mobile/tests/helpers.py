"""Shared helpers and payload builders for the mobile sync API tests."""
import uuid

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


def new_uuid():
    """A local_uuid the way the mobile app generates it (max 36 chars)."""
    return str(uuid.uuid4())


def participant_payload(**overrides):
    payload = {
        "local_uuid": new_uuid(),
        "site_code": "MUHAS",
        "participant_type": "CASE",
        "date_of_recruitment": "2026-06-21",
        "year_of_birth": 1990,
        "sex": "MALE",
        "region": "Dar es Salaam",
        "district": "Ilala",
        "phone_number": "0712345678",
    }
    payload.update(overrides)
    return payload


def clinical_data_payload(participant_server_id, **overrides):
    payload = {
        "local_uuid": new_uuid(),
        "participant_server_id": participant_server_id,
        "primary_diagnosis": "TB",
        "date_of_diagnosis": "2026-06-10",
        "laboratory_tests_performed": ["GENEXPERT", "SMEAR"],
        "comorbidities": ["DIABETES"],
        "comorbidity_duration_map": {"DIABETES": {"years": 2}},
        "vaccination_status": ["BCG"],
    }
    payload.update(overrides)
    return payload


def medications_payload(clinical_data_server_id, **overrides):
    payload = {
        "local_uuid": new_uuid(),
        "clinical_data_server_id": clinical_data_server_id,
        "medications": [
            {
                "medication_name": "RIFAMPICIN",
                "dose_frequency": "OD",
                "dose_duration": "6_MONTHS",
                "display_order": 1,
            },
            {
                "medication_name": "ISONIAZID",
                "dose_frequency": "OD",
                "dose_duration": "6_MONTHS",
                "display_order": 2,
            },
        ],
    }
    payload.update(overrides)
    return payload


def cough_recording_payload(**overrides):
    """Non-file multipart fields for a cough recording."""
    payload = {
        "local_uuid": new_uuid(),
        "patient_type": "CASE",
        "timepoint": "BASELINE",
        "sample_number": 1,
        "setting": "FACILITY",
        "recording_location": "WARD",
        "cough_type": "VOLUNTARY",
        "cough_date": "2026-06-21",
        "cough_time": "08:30:00",
        "sampling_rate_khz": 48.0,
        "distance_cm": 15,
        "facility_name": "MUHAS Clinic",
        "device_used": "Samsung A14",
        "checklist_count_1_to_10_done": True,
        "checklist_3_deep_breaths_done": True,
        "checklist_5_cough_bursts_done": True,
        "five_min_gap_confirmed": True,
    }
    payload.update(overrides)
    return payload


class AuthenticatedAPITestCase(APITestCase):
    """Base test case with a logged-in field researcher."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="fieldworker",
            password="StrongPass!234",
            first_name="Field",
            last_name="Worker",
        )

    def setUp(self):
        self.client.force_authenticate(user=self.user)
