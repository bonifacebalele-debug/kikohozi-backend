import logging
from django.db import transaction, IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.mobile.auth import CsrfExemptSessionAuthentication
from apps.mobile.models import Participant, ClinicalData, ClinicalMedication, CoughRecording
from apps.mobile.serializers import (
    ParticipantSyncSerializer,
    ClinicalDataSyncSerializer,
    ClinicalMedicationsSyncSerializer,
    CoughRecordingSyncSerializer,
)

logger = logging.getLogger(__name__)


def _log(request, msg, *args):
    logger.info(msg, *args, extra={"request_id": getattr(request, "request_id", "-")})


def _participant_response(participant):
    """
    Response shape for participant sync.
    Redundant keys ensure the app's SyncResponseParsers.extractParticipantServerId()
    always finds the server ID regardless of which key it checks first.
    """
    return {
        "success": True,
        "message": "Participant synced successfully.",
        "server_id": participant.pk,
        "server_participant_id": participant.pk,
        "generated_participant_id": participant.generated_participant_id,
        "participant_id": participant.generated_participant_id,
        "data": {
            "server_id": participant.pk,
            "server_participant_id": participant.pk,
            "generated_participant_id": participant.generated_participant_id,
            "participant_id": participant.generated_participant_id,
            "participant": {
                "id": participant.pk,
                "server_id": participant.pk,
                "generated_participant_id": participant.generated_participant_id,
                "participant_id": participant.generated_participant_id,
            },
        },
    }


def _clinical_data_response(clinical_data):
    """
    Response shape for clinical data sync.
    Redundant keys ensure the app's SyncResponseParsers.extractClinicalServerId()
    always finds the server ID.
    """
    return {
        "success": True,
        "message": "Clinical data synced successfully.",
        "server_id": clinical_data.pk,
        "clinical_data_server_id": clinical_data.pk,
        "participant_server_id": clinical_data.participant_id,
        "participant_id": clinical_data.participant.generated_participant_id,
        "data": {
            "server_id": clinical_data.pk,
            "clinical_data_server_id": clinical_data.pk,
            "participant_server_id": clinical_data.participant_id,
            "participant_id": clinical_data.participant.generated_participant_id,
            "clinical_data": {
                "id": clinical_data.pk,
                "server_id": clinical_data.pk,
                "participant_server_id": clinical_data.participant_id,
                "participant_id": clinical_data.participant.generated_participant_id,
            },
        },
    }


def _generate_participant_id(participant):
    site = (participant.site_code or "UNK")[:4].upper()
    year = participant.date_of_recruitment.year if participant.date_of_recruitment else "0000"
    return f"KIK-{site}-{year}-{participant.pk:05d}"


class SyncParticipantView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = ParticipantSyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        local_uuid = data.pop("local_uuid")

        existing = Participant.objects.filter(local_uuid=local_uuid).first()
        if existing:
            _log(request, "Participant already synced local_uuid=%s id=%d", local_uuid, existing.pk)
            return Response(_participant_response(existing))

        try:
            with transaction.atomic():
                participant = Participant.objects.create(
                    local_uuid=local_uuid,
                    synced_by=request.user,
                    **data,
                )
                participant.generated_participant_id = _generate_participant_id(participant)
                participant.save(update_fields=["generated_participant_id"])
        except IntegrityError:
            # Race: a concurrent request for the same draft won the unique constraint.
            # Recover idempotently by returning the row that did get created.
            existing = Participant.objects.filter(local_uuid=local_uuid).first()
            if existing:
                _log(request, "Participant race resolved local_uuid=%s id=%d", local_uuid, existing.pk)
                return Response(_participant_response(existing))
            raise

        _log(request, "Participant synced id=%d pid=%s", participant.pk, participant.generated_participant_id)

        return Response(_participant_response(participant), status=status.HTTP_201_CREATED)


class SyncClinicalDataView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = ClinicalDataSyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        local_uuid = data.pop("local_uuid")
        participant_server_id = data.pop("participant_server_id")

        existing = ClinicalData.objects.filter(local_uuid=local_uuid).select_related("participant").first()
        if existing:
            _log(request, "ClinicalData already synced local_uuid=%s id=%d", local_uuid, existing.pk)
            return Response(_clinical_data_response(existing))

        try:
            participant = Participant.objects.get(pk=participant_server_id)
        except Participant.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": f"Participant with id {participant_server_id} not found.",
                    "errors": {"participant_server_id": ["Participant not found."]},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            with transaction.atomic():
                clinical_data = ClinicalData.objects.create(
                    local_uuid=local_uuid,
                    participant=participant,
                    synced_by=request.user,
                    **data,
                )
        except IntegrityError:
            existing = ClinicalData.objects.filter(local_uuid=local_uuid).select_related("participant").first()
            if existing:
                _log(request, "ClinicalData race resolved local_uuid=%s id=%d", local_uuid, existing.pk)
                return Response(_clinical_data_response(existing))
            raise

        _log(request, "ClinicalData synced id=%d participant=%d", clinical_data.pk, participant.pk)

        return Response(_clinical_data_response(clinical_data), status=status.HTTP_201_CREATED)


class SyncClinicalMedicationsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = ClinicalMedicationsSyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        local_uuid = data["local_uuid"]
        clinical_data_server_id = data["clinical_data_server_id"]
        medications_data = data["medications"]

        try:
            with transaction.atomic():
                # Lock the parent row so two concurrent batch syncs can't both pass
                # the idempotency check and double-insert the medications.
                clinical_data = (
                    ClinicalData.objects.select_for_update()
                    .get(pk=clinical_data_server_id)
                )

                already_synced = clinical_data.medications_local_uuid == local_uuid
                if not already_synced:
                    clinical_data.medications.all().delete()
                    ClinicalMedication.objects.bulk_create([
                        ClinicalMedication(
                            clinical_data=clinical_data,
                            medication_name=med.get("medication_name") or "",
                            medication_other=med.get("medication_other") or "",
                            dose_frequency=med.get("dose_frequency") or "",
                            dose_duration=med.get("dose_duration") or "",
                            display_order=med.get("display_order", 1),
                        )
                        for med in medications_data
                    ])
                    clinical_data.medications_local_uuid = local_uuid
                    clinical_data.save(update_fields=["medications_local_uuid"])
        except ClinicalData.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": f"Clinical data record {clinical_data_server_id} not found.",
                    "errors": {"clinical_data_server_id": ["Clinical data record not found."]},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Idempotency: same batch already saved
        if already_synced:
            _log(request, "Medications already synced local_uuid=%s", local_uuid)
            return Response({
                "success": True,
                "message": "Clinical medications already synced.",
                "data": {
                    "clinical_data": {
                        "id": clinical_data.pk,
                        "participant_server_id": clinical_data.participant_id,
                    }
                },
            })

        _log(
            request,
            "Medications synced clinical_data=%d count=%d",
            clinical_data.pk,
            len(medications_data),
        )

        return Response(
            {
                "success": True,
                "message": "Clinical medications synced successfully.",
                "data": {
                    "clinical_data": {
                        "id": clinical_data.pk,
                        "participant_server_id": clinical_data.participant_id,
                    }
                },
            },
            status=status.HTTP_201_CREATED,
        )


class SyncCoughRecordingView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        # request.data is a QueryDict that already merges multipart form fields and
        # uploaded files. It must be passed straight through: flattening it with
        # {**request.data} would leak QueryDict's internal list storage and make every
        # field arrive as a single-element list, failing validation.
        serializer = CoughRecordingSyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        local_uuid = data.pop("local_uuid")
        participant_server_id = data.pop("participant_server_id", None)
        participant_id_str = data.pop("participant_id", None)
        audio_file = data.pop("audio_file")

        existing = CoughRecording.objects.filter(local_uuid=local_uuid).first()
        if existing:
            _log(request, "CoughRecording already synced local_uuid=%s id=%d", local_uuid, existing.pk)
            return Response({
                "success": True,
                "message": "Cough recording already synced.",
                "data": {
                    "cough_recording": {
                        "id": existing.pk,
                        "participant_server_id": existing.participant_id,
                    }
                },
            })

        participant = None
        if participant_server_id:
            participant = Participant.objects.filter(pk=participant_server_id).first()
        if participant is None and participant_id_str:
            participant = Participant.objects.filter(
                generated_participant_id=participant_id_str
            ).first()

        if participant is None:
            return Response(
                {
                    "success": False,
                    "message": "Participant not found.",
                    "errors": {"participant_server_id": ["Participant not found."]},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            with transaction.atomic():
                recording = CoughRecording.objects.create(
                    local_uuid=local_uuid,
                    participant=participant,
                    synced_by=request.user,
                    audio_file=audio_file,
                    audio_file_name=audio_file.name,
                    audio_file_size_bytes=audio_file.size,
                    **data,
                )
        except IntegrityError:
            existing = CoughRecording.objects.filter(local_uuid=local_uuid).first()
            if existing:
                _log(request, "CoughRecording race resolved local_uuid=%s id=%d", local_uuid, existing.pk)
                return Response({
                    "success": True,
                    "message": "Cough recording already synced.",
                    "data": {
                        "cough_recording": {
                            "id": existing.pk,
                            "participant_server_id": existing.participant_id,
                        }
                    },
                })
            raise

        _log(request, "CoughRecording synced id=%d participant=%d", recording.pk, participant.pk)

        return Response(
            {
                "success": True,
                "message": "Cough recording synced successfully.",
                "data": {
                    "cough_recording": {
                        "id": recording.pk,
                        "participant_server_id": participant.pk,
                    }
                },
            },
            status=status.HTTP_201_CREATED,
        )
