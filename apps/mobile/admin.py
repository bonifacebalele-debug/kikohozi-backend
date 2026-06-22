from django.contrib import admin
from .models import Participant, ClinicalData, ClinicalMedication, CoughRecording


class ClinicalDataInline(admin.TabularInline):
    model = ClinicalData
    extra = 0
    show_change_link = True
    fields = ("primary_diagnosis", "date_of_diagnosis", "synced_by", "created_at")
    readonly_fields = ("created_at",)


class CoughRecordingInline(admin.TabularInline):
    model = CoughRecording
    extra = 0
    show_change_link = True
    fields = ("patient_type", "timepoint", "sample_number", "cough_date", "qc_status")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "generated_participant_id", "site_code", "participant_type",
        "sex", "region", "synced_by", "created_at",
    )
    list_filter = ("site_code", "participant_type", "sex", "region")
    search_fields = ("generated_participant_id", "local_uuid", "phone_number")
    readonly_fields = ("local_uuid", "generated_participant_id", "created_at", "updated_at")
    inlines = [ClinicalDataInline, CoughRecordingInline]

    fieldsets = (
        ("Identifiers", {
            "fields": ("local_uuid", "generated_participant_id", "synced_by"),
        }),
        ("Enrolment", {
            "fields": ("site_code", "participant_type", "date_of_recruitment"),
        }),
        ("Demographics", {
            "fields": ("year_of_birth", "sex", "region", "district", "ward", "street", "phone_number"),
        }),
        ("Household", {
            "fields": ("residence_type", "house_type", "household_size"),
            "classes": ("collapse",),
        }),
        ("Socioeconomic", {
            "fields": ("occupation", "education_level"),
            "classes": ("collapse",),
        }),
        ("Lifestyle", {
            "fields": (
                "ever_smoked_tobacco", "smoke_nowadays", "cigarettes_per_day",
                "vaping_status", "alcohol_use", "alcohol_bottles_per_week",
                "exposure_to_pollutants",
            ),
            "classes": ("collapse",),
        }),
        ("TB History", {
            "fields": (
                "tb_contact_history", "tb_relation_with_patient",
                "tb_year_of_past_exposure", "tb_current_exposure", "tb_duration_of_exposure",
            ),
            "classes": ("collapse",),
        }),
        ("Asthma History", {
            "fields": ("family_history_of_asthma", "asthma_relation"),
            "classes": ("collapse",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


class ClinicalMedicationInline(admin.TabularInline):
    model = ClinicalMedication
    extra = 0
    fields = ("display_order", "medication_name", "medication_other", "dose_frequency", "dose_duration")


@admin.register(ClinicalData)
class ClinicalDataAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "participant", "primary_diagnosis", "date_of_diagnosis", "synced_by", "created_at",
    )
    list_filter = ("primary_diagnosis",)
    search_fields = ("local_uuid", "participant__generated_participant_id")
    readonly_fields = ("local_uuid", "created_at", "updated_at")
    inlines = [ClinicalMedicationInline]


@admin.register(CoughRecording)
class CoughRecordingAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "participant", "patient_type", "timepoint",
        "sample_number", "cough_date", "qc_status", "synced_by",
    )
    list_filter = ("patient_type", "timepoint", "qc_status", "setting")
    search_fields = ("local_uuid", "participant__generated_participant_id")
    readonly_fields = (
        "local_uuid", "audio_file_name", "audio_file_size_bytes", "created_at", "updated_at",
    )
