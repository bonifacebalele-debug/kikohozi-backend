from django.db import models
from django.conf import settings


class Participant(models.Model):
    local_uuid = models.CharField(max_length=36, unique=True, db_index=True)
    generated_participant_id = models.CharField(max_length=50, unique=True, blank=True)
    synced_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="synced_participants",
    )

    site_code = models.CharField(max_length=50)
    participant_type = models.CharField(max_length=50)
    date_of_recruitment = models.DateField()
    year_of_birth = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, blank=True)

    region = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    ward = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    residence_type = models.CharField(max_length=50, blank=True)
    house_type = models.CharField(max_length=50, blank=True)
    household_size = models.IntegerField(null=True, blank=True)

    occupation = models.CharField(max_length=100, blank=True)
    education_level = models.CharField(max_length=50, blank=True)

    ever_smoked_tobacco = models.CharField(max_length=10, blank=True)
    smoke_nowadays = models.CharField(max_length=10, blank=True)
    cigarettes_per_day = models.IntegerField(null=True, blank=True)

    vaping_status = models.CharField(max_length=50, blank=True)
    alcohol_use = models.CharField(max_length=50, blank=True)
    alcohol_bottles_per_week = models.IntegerField(null=True, blank=True)
    exposure_to_pollutants = models.CharField(max_length=50, blank=True)

    tb_contact_history = models.CharField(max_length=10, blank=True)
    tb_relation_with_patient = models.CharField(max_length=50, blank=True)
    tb_year_of_past_exposure = models.CharField(max_length=50, blank=True)
    tb_current_exposure = models.CharField(max_length=10, blank=True)
    tb_duration_of_exposure = models.CharField(max_length=50, blank=True)

    family_history_of_asthma = models.CharField(max_length=10, blank=True)
    asthma_relation = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["site_code"]),
            models.Index(fields=["participant_type"]),
            models.Index(fields=["date_of_recruitment"]),
        ]

    def __str__(self):
        return self.generated_participant_id or f"Participant #{self.pk}"


class ClinicalData(models.Model):
    local_uuid = models.CharField(max_length=36, unique=True, db_index=True)
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="clinical_records",
    )
    synced_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="synced_clinical_data",
    )

    primary_diagnosis = models.CharField(max_length=50)
    date_of_diagnosis = models.DateField(null=True, blank=True)
    diagnosis_report = models.CharField(max_length=50, blank=True)
    mechanism_of_diagnosis = models.CharField(max_length=50, blank=True)

    laboratory_tests_performed = models.JSONField(default=list, blank=True)
    lab_tests_other_description = models.TextField(blank=True)

    treatment_start_date = models.DateField(null=True, blank=True)
    current_treatment_regimen = models.CharField(max_length=100, blank=True)
    current_treatment_regimen_other = models.CharField(max_length=200, blank=True)
    dose_frequency = models.CharField(max_length=50, blank=True)
    dose_duration = models.CharField(max_length=50, blank=True)

    comorbidities = models.JSONField(default=list, blank=True)
    comorbidity_duration_map = models.JSONField(default=dict, blank=True)
    comorbidity_other_name = models.CharField(max_length=200, blank=True)
    comorbidity_other_years = models.IntegerField(null=True, blank=True)
    comorbidity_other_months = models.IntegerField(null=True, blank=True)

    currently_coughing = models.CharField(max_length=20, blank=True)
    currently_coughing_duration_days = models.IntegerField(null=True, blank=True)
    currently_coughing_duration_weeks = models.IntegerField(null=True, blank=True)
    currently_coughing_duration_months = models.IntegerField(null=True, blank=True)

    cough_type = models.CharField(max_length=50, blank=True)
    sputum_production = models.CharField(max_length=50, blank=True)
    sputum_colour = models.CharField(max_length=50, blank=True)
    sputum_volume = models.CharField(max_length=50, blank=True)
    cough_frequency = models.CharField(max_length=50, blank=True)

    difficulty_in_breathing = models.CharField(max_length=50, blank=True)
    chest_pain = models.CharField(max_length=20, blank=True)
    chest_pain_duration_days = models.IntegerField(null=True, blank=True)
    chest_pain_duration_weeks = models.IntegerField(null=True, blank=True)
    chest_pain_duration_months = models.IntegerField(null=True, blank=True)

    wheezing = models.CharField(max_length=20, blank=True)
    wheezing_duration_days = models.IntegerField(null=True, blank=True)
    wheezing_duration_weeks = models.IntegerField(null=True, blank=True)
    wheezing_duration_months = models.IntegerField(null=True, blank=True)

    hospital_admission_history = models.CharField(max_length=10, blank=True)
    hospital_admission_count = models.IntegerField(null=True, blank=True)
    hospital_admission_diagnoses = models.TextField(blank=True)

    vaccination_status = models.JSONField(default=list, blank=True)

    # Idempotency key for the medications batch linked to this record
    medications_local_uuid = models.CharField(max_length=36, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["participant", "primary_diagnosis"]),
        ]

    def __str__(self):
        return f"Clinical record #{self.pk} — {self.participant}"


class ClinicalMedication(models.Model):
    clinical_data = models.ForeignKey(
        ClinicalData,
        on_delete=models.CASCADE,
        related_name="medications",
    )
    medication_name = models.CharField(max_length=100, blank=True)
    medication_other = models.CharField(max_length=200, blank=True)
    dose_frequency = models.CharField(max_length=50, blank=True)
    dose_duration = models.CharField(max_length=50, blank=True)
    display_order = models.IntegerField(default=1)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.medication_name or self.medication_other or f"Medication #{self.pk}"


def cough_recording_upload_path(instance, filename):
    date = instance.cough_date or "unknown"
    return f"cough_recordings/{instance.participant_id}/{date}/{filename}"


class CoughRecording(models.Model):
    local_uuid = models.CharField(max_length=36, unique=True, db_index=True)
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="cough_recordings",
    )
    synced_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="synced_cough_recordings",
    )

    patient_type = models.CharField(max_length=50)
    timepoint = models.CharField(max_length=50)
    sample_number = models.IntegerField(default=1)
    setting = models.CharField(max_length=50)
    recording_location = models.CharField(max_length=100)
    cough_type = models.CharField(max_length=50)
    cough_date = models.DateField()
    cough_time = models.TimeField()
    sampling_rate_khz = models.FloatField(default=48.0)
    distance_cm = models.IntegerField(default=15)

    facility_name = models.CharField(max_length=200, blank=True)
    community_event_name = models.CharField(max_length=200, blank=True)

    audio_file = models.FileField(upload_to=cough_recording_upload_path)
    audio_file_name = models.CharField(max_length=255)
    audio_file_size_bytes = models.BigIntegerField(null=True, blank=True)
    device_used = models.CharField(max_length=200, blank=True)

    checklist_count_1_to_10_done = models.BooleanField(default=False)
    checklist_3_deep_breaths_done = models.BooleanField(default=False)
    checklist_5_cough_bursts_done = models.BooleanField(default=False)
    five_min_gap_confirmed = models.BooleanField(default=False)

    qc_status = models.CharField(max_length=20, default="PENDING")
    qc_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["participant", "cough_date"]),
            models.Index(fields=["qc_status"]),
        ]

    def __str__(self):
        return f"Cough recording #{self.pk} — {self.participant}"
