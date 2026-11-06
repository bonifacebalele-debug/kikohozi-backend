"""Tests for consent-form sync: multipart image upload attached to a synced participant."""
import hashlib
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status

from apps.mobile.models import Participant
from apps.mobile.tests.helpers import AuthenticatedAPITestCase, participant_payload

PARTICIPANT_URL = "/api/mobile/sync/participant/"
URL = "/api/mobile/sync/consent-form/"

JPEG_BYTES = b"\xff\xd8\xff\xe0" + b"\x00" * 64 + b"\xff\xd9"
OTHER_JPEG_BYTES = b"\xff\xd8\xff\xe1" + b"\x01" * 64 + b"\xff\xd9"
PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64

_MEDIA_ROOT = tempfile.mkdtemp(prefix="kikohozi-test-media-")


def jpeg_file(content=JPEG_BYTES, name="consent.jpg"):
    return SimpleUploadedFile(name, content, content_type="image/jpeg")


@override_settings(MEDIA_ROOT=_MEDIA_ROOT)
class ConsentFormSyncTests(AuthenticatedAPITestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def _create_participant(self):
        return self.client.post(
            PARTICIPANT_URL, participant_payload(), format="json"
        ).data

    def test_uploads_consent_form_by_server_id(self):
        participant = self._create_participant()
        response = self.client.post(
            URL,
            {"participant_server_id": participant["server_id"], "consent_form_photo": jpeg_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved = Participant.objects.get(pk=participant["server_id"])
        self.assertTrue(saved.consent_form_photo.name.startswith(f"consent_forms/{saved.pk}/"))
        self.assertEqual(saved.consent_form_checksum_sha256, hashlib.sha256(JPEG_BYTES).hexdigest())
        self.assertIsNotNone(saved.consent_form_uploaded_at)

    def test_uploads_consent_form_by_generated_participant_id(self):
        participant = self._create_participant()
        response = self.client.post(
            URL,
            {
                "participant_id": participant["generated_participant_id"],
                "consent_form_photo": SimpleUploadedFile("consent.png", PNG_BYTES, "image/png"),
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Participant.objects.get(pk=participant["server_id"]).consent_form_photo)

    def test_same_image_twice_is_idempotent(self):
        participant = self._create_participant()
        first = self.client.post(
            URL,
            {"participant_server_id": participant["server_id"], "consent_form_photo": jpeg_file()},
            format="multipart",
        )
        first_name = Participant.objects.get(pk=participant["server_id"]).consent_form_photo.name
        second = self.client.post(
            URL,
            {"participant_server_id": participant["server_id"], "consent_form_photo": jpeg_file()},
            format="multipart",
        )

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        saved = Participant.objects.get(pk=participant["server_id"])
        self.assertEqual(saved.consent_form_photo.name, first_name)

    def test_new_image_replaces_previous_one(self):
        participant = self._create_participant()
        self.client.post(
            URL,
            {"participant_server_id": participant["server_id"], "consent_form_photo": jpeg_file()},
            format="multipart",
        )
        old_name = Participant.objects.get(pk=participant["server_id"]).consent_form_photo.name

        response = self.client.post(
            URL,
            {
                "participant_server_id": participant["server_id"],
                "consent_form_photo": jpeg_file(OTHER_JPEG_BYTES),
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved = Participant.objects.get(pk=participant["server_id"])
        self.assertEqual(saved.consent_form_checksum_sha256, hashlib.sha256(OTHER_JPEG_BYTES).hexdigest())
        self.assertFalse(saved.consent_form_photo.storage.exists(old_name))

    def test_rejects_non_image_file(self):
        participant = self._create_participant()
        response = self.client.post(
            URL,
            {
                "participant_server_id": participant["server_id"],
                "consent_form_photo": SimpleUploadedFile("consent.jpg", b"not an image", "image/jpeg"),
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("consent_form_photo", response.data["errors"])
        self.assertFalse(Participant.objects.get(pk=participant["server_id"]).consent_form_photo)

    def test_rejects_empty_file(self):
        participant = self._create_participant()
        response = self.client.post(
            URL,
            {
                "participant_server_id": participant["server_id"],
                "consent_form_photo": SimpleUploadedFile("consent.jpg", b"", "image/jpeg"),
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requires_some_participant_reference(self):
        response = self.client.post(URL, {"consent_form_photo": jpeg_file()}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unknown_participant_returns_404(self):
        response = self.client.post(
            URL,
            {"participant_server_id": 999999, "consent_form_photo": jpeg_file()},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_requires_authentication(self):
        participant = self._create_participant()
        self.client.force_authenticate(user=None)
        response = self.client.post(
            URL,
            {"participant_server_id": participant["server_id"], "consent_form_photo": jpeg_file()},
            format="multipart",
        )
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
