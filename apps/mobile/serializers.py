from rest_framework import serializers


class ParticipantSyncSerializer(serializers.Serializer):
    local_uuid = serializers.CharField(max_length=36)
    site_code = serializers.CharField(max_length=50)
    participant_type = serializers.CharField(max_length=50)
    date_of_recruitment = serializers.DateField()
    year_of_birth = serializers.IntegerField(required=False, allow_null=True)
    sex = serializers.CharField(max_length=10, required=False, allow_blank=True)

    region = serializers.CharField(max_length=100, required=False, allow_blank=True)
    district = serializers.CharField(max_length=100, required=False, allow_blank=True)
    ward = serializers.CharField(max_length=100, required=False, allow_blank=True)
    street = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)

    residence_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    house_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    household_size = serializers.IntegerField(required=False, allow_null=True)

    occupation = serializers.CharField(max_length=100, required=False, allow_blank=True)
    education_level = serializers.CharField(max_length=50, required=False, allow_blank=True)

    ever_smoked_tobacco = serializers.CharField(max_length=10, required=False, allow_blank=True)
    smoke_nowadays = serializers.CharField(max_length=10, required=False, allow_blank=True)
    cigarettes_per_day = serializers.IntegerField(required=False, allow_null=True)

    vaping_status = serializers.CharField(max_length=50, required=False, allow_blank=True)
    alcohol_use = serializers.CharField(max_length=50, required=False, allow_blank=True)
    alcohol_bottles_per_week = serializers.IntegerField(required=False, allow_null=True)
    exposure_to_pollutants = serializers.CharField(max_length=50, required=False, allow_blank=True)

    tb_contact_history = serializers.CharField(max_length=10, required=False, allow_blank=True)
    tb_relation_with_patient = serializers.CharField(max_length=50, required=False, allow_blank=True)
    tb_year_of_past_exposure = serializers.CharField(max_length=50, required=False, allow_blank=True)
    tb_current_exposure = serializers.CharField(max_length=10, required=False, allow_blank=True)
    tb_duration_of_exposure = serializers.CharField(max_length=50, required=False, allow_blank=True)

    family_history_of_asthma = serializers.CharField(max_length=10, required=False, allow_blank=True)
    asthma_relation = serializers.CharField(max_length=100, required=False, allow_blank=True)


class ConsentFormSyncSerializer(serializers.Serializer):
    participant_server_id = serializers.IntegerField(required=False, allow_null=True)
    participant_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
    consent_form_photo = serializers.FileField()

    def validate_consent_form_photo(self, value):
        if value.size == 0:
            raise serializers.ValidationError("The consent form photo is empty.")
        if value.size > 10_485_760:
            raise serializers.ValidationError("Consent form photo exceeds the 10 MB limit.")
        # Check magic bytes rather than trusting the filename or content type.
        value.seek(0)
        header = value.read(8)
        value.seek(0)
        if not (header.startswith(b"\xff\xd8\xff") or header.startswith(b"\x89PNG\r\n\x1a\n")):
            raise serializers.ValidationError("Only JPEG or PNG images are accepted.")
        return value

    def validate(self, data):
        if not data.get("participant_server_id") and not data.get("participant_id"):
            raise serializers.ValidationError(
                "Either participant_server_id or participant_id is required."
            )
        return data


class ClinicalDataSyncSerializer(serializers.Serializer):
    local_uuid = serializers.CharField(max_length=36)
    participant_server_id = serializers.IntegerField()
    primary_diagnosis = serializers.CharField(max_length=50)

    date_of_diagnosis = serializers.DateField(required=False, allow_null=True)
    diagnosis_report = serializers.CharField(max_length=50, required=False, allow_blank=True)
    mechanism_of_diagnosis = serializers.CharField(max_length=50, required=False, allow_blank=True)

    laboratory_tests_performed = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    lab_tests_other_description = serializers.CharField(required=False, allow_blank=True, default="")

    treatment_start_date = serializers.DateField(required=False, allow_null=True)
    current_treatment_regimen = serializers.CharField(max_length=100, required=False, allow_blank=True)
    current_treatment_regimen_other = serializers.CharField(max_length=200, required=False, allow_blank=True)
    dose_frequency = serializers.CharField(max_length=50, required=False, allow_blank=True)
    dose_duration = serializers.CharField(max_length=50, required=False, allow_blank=True)

    comorbidities = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    comorbidity_duration_map = serializers.DictField(required=False, default=dict)
    comorbidity_other_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    comorbidity_other_years = serializers.IntegerField(required=False, allow_null=True)
    comorbidity_other_months = serializers.IntegerField(required=False, allow_null=True)

    currently_coughing = serializers.CharField(max_length=20, required=False, allow_blank=True)
    currently_coughing_duration_days = serializers.IntegerField(required=False, allow_null=True)
    currently_coughing_duration_weeks = serializers.IntegerField(required=False, allow_null=True)
    currently_coughing_duration_months = serializers.IntegerField(required=False, allow_null=True)

    cough_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    sputum_production = serializers.CharField(max_length=50, required=False, allow_blank=True)
    sputum_colour = serializers.CharField(max_length=50, required=False, allow_blank=True)
    sputum_volume = serializers.CharField(max_length=50, required=False, allow_blank=True)
    cough_frequency = serializers.CharField(max_length=50, required=False, allow_blank=True)

    difficulty_in_breathing = serializers.CharField(max_length=50, required=False, allow_blank=True)
    chest_pain = serializers.CharField(max_length=20, required=False, allow_blank=True)
    chest_pain_duration_days = serializers.IntegerField(required=False, allow_null=True)
    chest_pain_duration_weeks = serializers.IntegerField(required=False, allow_null=True)
    chest_pain_duration_months = serializers.IntegerField(required=False, allow_null=True)

    wheezing = serializers.CharField(max_length=20, required=False, allow_blank=True)
    wheezing_duration_days = serializers.IntegerField(required=False, allow_null=True)
    wheezing_duration_weeks = serializers.IntegerField(required=False, allow_null=True)
    wheezing_duration_months = serializers.IntegerField(required=False, allow_null=True)

    hospital_admission_history = serializers.CharField(max_length=10, required=False, allow_blank=True)
    hospital_admission_count = serializers.IntegerField(required=False, allow_null=True)
    hospital_admission_diagnoses = serializers.CharField(required=False, allow_blank=True, default="")

    vaccination_status = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )


class MedicationItemSerializer(serializers.Serializer):
    medication_name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    medication_other = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    dose_frequency = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    dose_duration = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    display_order = serializers.IntegerField(required=False, default=1)


class ClinicalMedicationsSyncSerializer(serializers.Serializer):
    local_uuid = serializers.CharField(max_length=36)
    clinical_data_server_id = serializers.IntegerField()
    # allow_empty=False guards against an empty batch silently wiping existing rows.
    medications = MedicationItemSerializer(many=True, allow_empty=False)


class CoughRecordingSyncSerializer(serializers.Serializer):
    local_uuid = serializers.CharField(max_length=36)
    participant_server_id = serializers.IntegerField(required=False, allow_null=True)
    participant_id = serializers.CharField(max_length=50, required=False, allow_blank=True)

    patient_type = serializers.CharField(max_length=50)
    timepoint = serializers.CharField(max_length=50)
    sample_number = serializers.IntegerField(default=1)
    setting = serializers.CharField(max_length=50)
    recording_location = serializers.CharField(max_length=100)
    cough_type = serializers.CharField(max_length=50)
    cough_date = serializers.DateField()
    cough_time = serializers.TimeField()
    sampling_rate_khz = serializers.FloatField(default=48.0)
    distance_cm = serializers.IntegerField(default=15)

    facility_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    community_event_name = serializers.CharField(max_length=200, required=False, allow_blank=True)

    device_used = serializers.CharField(max_length=200, required=False, allow_blank=True)
    recorded_by = serializers.CharField(max_length=150, required=False, allow_blank=True)
    audio_file = serializers.FileField()

    checklist_count_1_to_10_done = serializers.BooleanField(required=False, default=False)
    checklist_3_deep_breaths_done = serializers.BooleanField(required=False, default=False)
    checklist_5_cough_bursts_done = serializers.BooleanField(required=False, default=False)
    five_min_gap_confirmed = serializers.BooleanField(required=False, default=False)

    def validate_audio_file(self, value):
        if not value.name.lower().endswith(".wav"):
            raise serializers.ValidationError("Only WAV audio files are accepted.")
        if value.size == 0:
            raise serializers.ValidationError("The audio file is empty.")
        if value.size > 52_428_800:
            raise serializers.ValidationError("Audio file exceeds the 50 MB limit.")
        return value

    def validate(self, data):
        if not data.get("participant_server_id") and not data.get("participant_id"):
            raise serializers.ValidationError(
                "Either participant_server_id or participant_id is required."
            )
        return data
