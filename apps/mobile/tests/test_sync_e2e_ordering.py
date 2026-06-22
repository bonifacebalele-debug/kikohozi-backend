"""End-to-end test of the full ordered sync chain a device performs in one session.

Participant -> Clinical Data -> Clinical Medication -> Cough Recording, with each
step feeding the server-generated id of the previous step into the next request.
"""
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status

from apps.mobile.models import (
    ClinicalData,
    ClinicalMedication,
    CoughRecording,
    Participant,
)
from apps.mobile.tests.helpers import (
    AuthenticatedAPITestCase,
    clinical_data_payload,
    cough_recording_payload,
    medications_payload,
    participant_payload,
)
from apps.mobile.tests.test_sync_cough_recording import WAV_BYTES

PARTICIPANT_URL = "/api/mobile/sync/participant/"
CLINICAL_URL = "/api/mobile/sync/clinical-data/"
MEDICATION_URL = "/api/mobile/sync/clinical-medications/"
COUGH_URL = "/api/mobile/sync/cough-recording/"

_MEDIA_ROOT = tempfile.mkdtemp(prefix="kikohozi-e2e-media-")


@override_settings(MEDIA_ROOT=_MEDIA_ROOT)
class OrderedSyncFlowTests(AuthenticatedAPITestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_full_chain_in_order(self):
        # Step 1/4 — participant
        p = self.client.post(PARTICIPANT_URL, participant_payload(), format="json")
        self.assertEqual(p.status_code, status.HTTP_201_CREATED)
        participant_id = p.data["server_id"]
        generated_id = p.data["generated_participant_id"]

        # Step 2/4 — clinical data references the participant server id
        cd = self.client.post(
            CLINICAL_URL, clinical_data_payload(participant_id), format="json"
        )
        self.assertEqual(cd.status_code, status.HTTP_201_CREATED)
        clinical_id = cd.data["server_id"]

        # Step 3/4 — medications reference the clinical-data server id
        med = self.client.post(
            MEDICATION_URL, medications_payload(clinical_id), format="json"
        )
        self.assertEqual(med.status_code, status.HTTP_201_CREATED)

        # Step 4/4 — cough recording references the participant server id + uploads WAV
        cough = self.client.post(
            COUGH_URL,
            cough_recording_payload(
                participant_server_id=participant_id,
                participant_id=generated_id,
                audio_file=SimpleUploadedFile("cough.wav", WAV_BYTES, "audio/wav"),
            ),
            format="multipart",
        )
        self.assertEqual(cough.status_code, status.HTTP_201_CREATED)

        # Everything is persisted and correctly linked.
        self.assertEqual(Participant.objects.count(), 1)
        self.assertEqual(ClinicalData.objects.count(), 1)
        self.assertEqual(ClinicalMedication.objects.count(), 2)
        self.assertEqual(CoughRecording.objects.count(), 1)

        participant = Participant.objects.get()
        self.assertEqual(participant.clinical_records.count(), 1)
        self.assertEqual(participant.cough_recordings.count(), 1)
        self.assertEqual(
            ClinicalData.objects.get().medications.count(), 2
        )

    def test_replaying_the_whole_chain_is_idempotent(self):
        """A device that retries an already-synced session creates no duplicates."""
        payloads = {}

        def run_chain():
            p = self.client.post(
                PARTICIPANT_URL,
                payloads.setdefault("p", participant_payload()),
                format="json",
            )
            participant_id = p.data["server_id"]
            cd = self.client.post(
                CLINICAL_URL,
                payloads.setdefault("cd", clinical_data_payload(participant_id)),
                format="json",
            )
            clinical_id = cd.data["server_id"]
            self.client.post(
                MEDICATION_URL,
                payloads.setdefault("med", medications_payload(clinical_id)),
                format="json",
            )
            cough = dict(payloads.setdefault("cough", cough_recording_payload(
                participant_server_id=participant_id,
            )))
            cough["audio_file"] = SimpleUploadedFile("cough.wav", WAV_BYTES, "audio/wav")
            self.client.post(COUGH_URL, cough, format="multipart")

        run_chain()
        run_chain()

        self.assertEqual(Participant.objects.count(), 1)
        self.assertEqual(ClinicalData.objects.count(), 1)
        self.assertEqual(ClinicalMedication.objects.count(), 2)
        self.assertEqual(CoughRecording.objects.count(), 1)
