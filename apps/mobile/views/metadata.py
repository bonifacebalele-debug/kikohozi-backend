from rest_framework.views import APIView
from rest_framework.response import Response
from apps.mobile.auth import CsrfExemptSessionAuthentication
import apps.mobile.choices as c


class MetadataView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        return Response({
            "success": True,
            "message": "Metadata retrieved.",
            "data": {
                "participant": {
                    "participant_types": c.PARTICIPANT_TYPES,
                    "site_choices": c.SITE_CHOICES,
                    "sex_choices": c.SEX_CHOICES,
                    "yes_no_choices": c.YES_NO_CHOICES,
                    "residence_type_choices": c.RESIDENCE_TYPE_CHOICES,
                    "house_type_choices": c.HOUSE_TYPE_CHOICES,
                    "occupation_choices": c.OCCUPATION_CHOICES,
                    "education_level_choices": c.EDUCATION_LEVEL_CHOICES,
                    "vaping_status_choices": c.VAPING_STATUS_CHOICES,
                    "alcohol_use_choices": c.ALCOHOL_USE_CHOICES,
                    "exposure_to_pollutants_choices": c.EXPOSURE_TO_POLLUTANTS_CHOICES,
                    "family_history_of_asthma_choices": c.FAMILY_HISTORY_OF_ASTHMA_CHOICES,
                    "tb_relation_with_patient_choices": c.TB_RELATION_WITH_PATIENT_CHOICES,
                    "tb_year_of_past_exposure_choices": c.TB_YEAR_OF_PAST_EXPOSURE_CHOICES,
                    "tb_duration_of_exposure_choices": c.TB_DURATION_OF_EXPOSURE_CHOICES,
                    "region_choices": c.REGION_CHOICES,
                    "region_to_districts": c.REGION_TO_DISTRICTS,
                },
                "clinical_data": {
                    "diagnosis_choices": c.DIAGNOSIS_CHOICES,
                    "diagnosis_report_choices": c.DIAGNOSIS_REPORT_CHOICES,
                    "mechanism_choices": c.MECHANISM_CHOICES,
                    "lab_test_choices": c.LAB_TEST_CHOICES,
                    "comorbidity_choices": c.COMORBIDITY_CHOICES,
                    "breathing_choices": c.BREATHING_CHOICES,
                    "vaccination_choices": c.VACCINATION_CHOICES,
                    "yes_no_choices": c.YES_NO_CHOICES,
                    "coughing_status_choices": c.COUGHING_STATUS_CHOICES,
                    "cough_type_choices": c.COUGH_TYPE_CHOICES,
                    "sputum_production_choices": c.SPUTUM_PRODUCTION_CHOICES,
                    "sputum_colour_choices": c.SPUTUM_COLOUR_CHOICES,
                    "sputum_volume_choices": c.SPUTUM_VOLUME_CHOICES,
                    "cough_frequency_choices": c.COUGH_FREQUENCY_CHOICES,
                    "present_absent_choices": c.PRESENT_ABSENT_CHOICES,
                    "treatment_regimen_choices": c.TREATMENT_REGIMEN_CHOICES,
                    "dose_frequency_choices": c.DOSE_FREQUENCY_CHOICES,
                    "dose_duration_choices": c.DOSE_DURATION_CHOICES,
                },
                "clinical_medication": {
                    "medication_choices": c.MEDICATION_CHOICES,
                    "dose_frequency_choices": c.DOSE_FREQUENCY_CHOICES,
                    "dose_duration_choices": c.DOSE_DURATION_CHOICES,
                },
                "cough_recording": {
                    "patient_type_choices": c.PATIENT_TYPE_CHOICES,
                    "timepoint_choices": c.TIMEPOINT_CHOICES,
                    "setting_choices": c.SETTING_CHOICES,
                    "recording_location_choices": c.RECORDING_LOCATION_CHOICES,
                    "cough_type_choices": c.COUGH_TYPE_CHOICES,
                    "qc_status_choices": c.QC_STATUS_CHOICES,
                    "allowed_audio_extensions": c.ALLOWED_AUDIO_EXTENSIONS,
                    "default_device_used": c.DEFAULT_DEVICE_USED,
                },
            },
        })
