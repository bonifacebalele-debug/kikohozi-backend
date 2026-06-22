"""Tests for cough-recording sync: multipart upload that depends on a synced participant."""
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status

from apps.mobile.models import CoughRecording
from apps.mobile.tests.helpers import (
    AuthenticatedAPITestCase,
    cough_recording_payload,
    participant_payload,
)

PARTICIPANT_URL = "/api/mobile/sync/participant/"
URL = "/api/mobile/sync/cough-recording/"

# Minimal but well-formed RIFF/WAVE header so the file is a plausible .wav.
WAV_BYTES = (
    b"RIFF" + (36).to_bytes(4, "little") + b"WAVE"
    b"fmt " + (16).to_bytes(4, "little")
    + (1).to_bytes(2, "little") + (1).to_bytes(2, "little")
    + (48000).to_bytes(4, "little") + (96000).to_bytes(4, "little")
    + (2).to_bytes(2, "little") + (16).to_bytes(2, "little")
    + b"data" + (0).to_bytes(4, "little")
)

_MEDIA_ROOT = tempfile.mkdtemp(prefix="kikohozi-test-media-")


def wav_file(name="cough.wav"):
    return SimpleUploadedFile(name, WAV_BYTES, content_type="audio/wav")


@override_settings(MEDIA_ROOT=_MEDIA_ROOT)
class CoughRecordingSyncTests(AuthenticatedAPITestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def _create_participant(self):
        return self.client.post(
            PARTICIPANT_URL, participant_payload(), format="json"
        ).data

    def test_uploads_recording_by_server_id(self):
        participant = self._create_participant()
        payload = cough_recording_payload(
            participant_server_id=participant["server_id"], audio_file=wav_file()
        )
        response = self.client.post(URL, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recording = CoughRecording.objects.get(local_uuid=payload["local_uuid"])
        self.assertEqual(recording.participant_id, participant["server_id"])
        self.assertEqual(recording.audio_file_size_bytes, len(WAV_BYTES))
        self.assertEqual(recording.synced_by, self.user)
        self.assertTrue(recording.audio_file.name.endswith(".wav"))

    def test_uploads_recording_by_generated_participant_id(self):
        participant = self._create_participant()
        payload = cough_recording_payload(
            participant_id=participant["generated_participant_id"],
            audio_file=wav_file(),
        )
        response = self.client.post(URL, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recording = CoughRecording.objects.get(local_uuid=payload["local_uuid"])
        self.assertEqual(recording.participant_id, participant["server_id"])

    def test_rejects_non_wav_file(self):
        participant = self._create_participant()
        payload = cough_recording_payload(
            participant_server_id=participant["server_id"],
            audio_file=SimpleUploadedFile("cough.mp3", b"not wav", "audio/mpeg"),
        )
        response = self.client.post(URL, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("audio_file", response.data["errors"])
        self.assertEqual(CoughRecording.objects.count(), 0)

    def test_rejects_empty_audio_file(self):
        participant = self._create_participant()
        payload = cough_recording_payload(
            participant_server_id=participant["server_id"],
            audio_file=SimpleUploadedFile("cough.wav", b"", "audio/wav"),
        )
        response = self.client.post(URL, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("audio_file", response.data["errors"])
        self.assertEqual(CoughRecording.objects.count(), 0)

    def test_requires_some_participant_reference(self):
        self._create_participant()
        payload = cough_recording_payload(audio_file=wav_file())  # no participant ref
        response = self.client.post(URL, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CoughRecording.objects.count(), 0)

    def test_unknown_participant_returns_404(self):
        payload = cough_recording_payload(
            participant_server_id=999999, audio_file=wav_file()
        )
        response = self.client.post(URL, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(CoughRecording.objects.count(), 0)

    def test_idempotent_on_duplicate_local_uuid(self):
        participant = self._create_participant()
        payload = cough_recording_payload(
            participant_server_id=participant["server_id"], audio_file=wav_file()
        )
        first = self.client.post(URL, payload, format="multipart")
        # Second attempt must re-send a fresh file object (the first was consumed).
        payload["audio_file"] = wav_file()
        second = self.client.post(URL, payload, format="multipart")

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(CoughRecording.objects.count(), 1)
