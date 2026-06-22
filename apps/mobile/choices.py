# All dropdown choices returned by the /metadata/ endpoint.
# Update values here to match your research protocol.

def _choice(value, label):
    return {"value": value, "label": label}


PARTICIPANT_TYPES = [
    _choice("TB", "Tuberculosis (TB)"),
    _choice("ASTHMA", "Asthma"),
    _choice("COPD", "COPD"),
    _choice("CONTROL", "Healthy Control"),
    _choice("OTHER", "Other"),
]

SITE_CHOICES = [
    _choice("MNH", "Muhimbili National Hospital"),
    _choice("MUHAS", "MUHAS Teaching Hospital"),
    _choice("AMANA", "Amana Regional Referral Hospital"),
    _choice("TEMEKE", "Temeke Regional Referral Hospital"),
    _choice("MWANANYAMALA", "Mwananyamala Regional Referral Hospital"),
    _choice("OTHER", "Other Site"),
]

SEX_CHOICES = [
    _choice("M", "Male"),
    _choice("F", "Female"),
]

YES_NO_CHOICES = [
    _choice("YES", "Yes"),
    _choice("NO", "No"),
]

RESIDENCE_TYPE_CHOICES = [
    _choice("URBAN", "Urban"),
    _choice("PERI_URBAN", "Peri-urban"),
    _choice("RURAL", "Rural"),
]

HOUSE_TYPE_CHOICES = [
    _choice("PERMANENT", "Permanent"),
    _choice("SEMI_PERMANENT", "Semi-permanent"),
    _choice("TEMPORARY", "Temporary"),
]

OCCUPATION_CHOICES = [
    _choice("EMPLOYED_FORMAL", "Formally Employed"),
    _choice("EMPLOYED_INFORMAL", "Informally Employed"),
    _choice("SELF_EMPLOYED", "Self-employed"),
    _choice("STUDENT", "Student"),
    _choice("UNEMPLOYED", "Unemployed"),
    _choice("RETIRED", "Retired"),
    _choice("OTHER", "Other"),
]

EDUCATION_LEVEL_CHOICES = [
    _choice("NONE", "No Formal Education"),
    _choice("PRIMARY", "Primary"),
    _choice("SECONDARY", "Secondary"),
    _choice("VOCATIONAL", "Vocational / Certificate"),
    _choice("UNIVERSITY", "University / Tertiary"),
    _choice("POSTGRADUATE", "Postgraduate"),
]

VAPING_STATUS_CHOICES = [
    _choice("NEVER", "Never vaped"),
    _choice("CURRENT", "Currently vaping"),
    _choice("FORMER", "Former vaper"),
]

ALCOHOL_USE_CHOICES = [
    _choice("NEVER", "Never"),
    _choice("OCCASIONAL", "Occasional"),
    _choice("REGULAR", "Regular"),
    _choice("HEAVY", "Heavy"),
    _choice("FORMER", "Former drinker"),
]

EXPOSURE_TO_POLLUTANTS_CHOICES = [
    _choice("NONE", "None"),
    _choice("BIOMASS_FUEL", "Biomass fuel / cooking smoke"),
    _choice("OCCUPATIONAL_DUST", "Occupational dust"),
    _choice("CHEMICAL_FUMES", "Chemical fumes"),
    _choice("OUTDOOR_AIR_POLLUTION", "Outdoor air pollution"),
    _choice("MULTIPLE", "Multiple sources"),
]

FAMILY_HISTORY_OF_ASTHMA_CHOICES = [
    _choice("NO", "No"),
    _choice("YES_FIRST_DEGREE", "Yes — first-degree relative"),
    _choice("YES_SECOND_DEGREE", "Yes — second-degree relative"),
    _choice("UNKNOWN", "Unknown"),
]

TB_RELATION_WITH_PATIENT_CHOICES = [
    _choice("HOUSEHOLD_MEMBER", "Household member"),
    _choice("CLOSE_CONTACT", "Close contact (non-household)"),
    _choice("WORK_COLLEAGUE", "Work colleague"),
    _choice("HEALTHCARE_WORKER", "Healthcare worker"),
    _choice("OTHER", "Other"),
]

TB_YEAR_OF_PAST_EXPOSURE_CHOICES = [
    _choice("LESS_THAN_1", "Less than 1 year ago"),
    _choice("1_TO_3", "1–3 years ago"),
    _choice("3_TO_5", "3–5 years ago"),
    _choice("MORE_THAN_5", "More than 5 years ago"),
    _choice("UNKNOWN", "Unknown"),
]

TB_DURATION_OF_EXPOSURE_CHOICES = [
    _choice("LESS_THAN_1_MONTH", "Less than 1 month"),
    _choice("1_TO_6_MONTHS", "1–6 months"),
    _choice("6_TO_12_MONTHS", "6–12 months"),
    _choice("MORE_THAN_1_YEAR", "More than 1 year"),
    _choice("UNKNOWN", "Unknown"),
]

REGION_CHOICES = [
    _choice("ARUSHA", "Arusha"),
    _choice("DAR_ES_SALAAM", "Dar es Salaam"),
    _choice("DODOMA", "Dodoma"),
    _choice("GEITA", "Geita"),
    _choice("IRINGA", "Iringa"),
    _choice("KAGERA", "Kagera"),
    _choice("KATAVI", "Katavi"),
    _choice("KIGOMA", "Kigoma"),
    _choice("KILIMANJARO", "Kilimanjaro"),
    _choice("LINDI", "Lindi"),
    _choice("MANYARA", "Manyara"),
    _choice("MARA", "Mara"),
    _choice("MBEYA", "Mbeya"),
    _choice("MOROGORO", "Morogoro"),
    _choice("MTWARA", "Mtwara"),
    _choice("MWANZA", "Mwanza"),
    _choice("NJOMBE", "Njombe"),
    _choice("PEMBA_NORTH", "Pemba North"),
    _choice("PEMBA_SOUTH", "Pemba South"),
    _choice("PWANI", "Pwani"),
    _choice("RUKWA", "Rukwa"),
    _choice("RUVUMA", "Ruvuma"),
    _choice("SHINYANGA", "Shinyanga"),
    _choice("SIMIYU", "Simiyu"),
    _choice("SINGIDA", "Singida"),
    _choice("SONGWE", "Songwe"),
    _choice("TABORA", "Tabora"),
    _choice("TANGA", "Tanga"),
    _choice("UNGUJA_NORTH", "Unguja North"),
    _choice("UNGUJA_SOUTH", "Unguja South"),
    _choice("UNGUJA_WEST", "Unguja West (Urban)"),
]

REGION_TO_DISTRICTS = {
    "DAR_ES_SALAAM": [
        _choice("ILALA", "Ilala"),
        _choice("KINONDONI", "Kinondoni"),
        _choice("TEMEKE", "Temeke"),
        _choice("UBUNGO", "Ubungo"),
        _choice("KIGAMBONI", "Kigamboni"),
    ],
    "ARUSHA": [
        _choice("ARUSHA_CITY", "Arusha City"),
        _choice("ARUSHA_DISTRICT", "Arusha District"),
        _choice("KARATU", "Karatu"),
        _choice("LONGIDO", "Longido"),
        _choice("MONDULI", "Monduli"),
        _choice("NGORONGORO", "Ngorongoro"),
    ],
    "KILIMANJARO": [
        _choice("MOSHI_URBAN", "Moshi Urban"),
        _choice("MOSHI_RURAL", "Moshi Rural"),
        _choice("HAI", "Hai"),
        _choice("ROMBO", "Rombo"),
        _choice("SIHA", "Siha"),
        _choice("SAME", "Same"),
        _choice("MWANGA", "Mwanga"),
    ],
}

# Clinical data choices
DIAGNOSIS_CHOICES = [
    _choice("TB", "Tuberculosis (TB)"),
    _choice("TB_RETREATMENT", "TB (Re-treatment)"),
    _choice("ASTHMA", "Asthma"),
    _choice("COPD", "COPD"),
    _choice("PNEUMONIA", "Pneumonia"),
    _choice("BRONCHIECTASIS", "Bronchiectasis"),
    _choice("LUNG_CANCER", "Lung Cancer"),
    _choice("COVID_19", "COVID-19"),
    _choice("OTHER", "Other"),
]

DIAGNOSIS_REPORT_CHOICES = [
    _choice("CONFIRMED", "Confirmed"),
    _choice("PROBABLE", "Probable"),
    _choice("SUSPECTED", "Suspected"),
]

MECHANISM_CHOICES = [
    _choice("SPUTUM_SMEAR", "Sputum smear microscopy"),
    _choice("SPUTUM_CULTURE", "Sputum culture"),
    _choice("GENE_XPERT", "GeneXpert MTB/RIF"),
    _choice("CHEST_XRAY", "Chest X-ray"),
    _choice("CT_SCAN", "CT scan"),
    _choice("CLINICAL_DIAGNOSIS", "Clinical diagnosis"),
    _choice("SPIROMETRY", "Spirometry"),
    _choice("OTHER", "Other"),
]

LAB_TEST_CHOICES = [
    _choice("SPUTUM_SMEAR", "Sputum smear microscopy"),
    _choice("SPUTUM_CULTURE", "Sputum culture"),
    _choice("GENE_XPERT", "GeneXpert MTB/RIF"),
    _choice("CHEST_XRAY", "Chest X-ray"),
    _choice("CT_SCAN", "CT scan"),
    _choice("SPIROMETRY", "Spirometry"),
    _choice("HIV_TEST", "HIV test"),
    _choice("BLOOD_COUNT", "Full blood count"),
    _choice("OTHER", "Other"),
]

COMORBIDITY_CHOICES = [
    _choice("HIV", "HIV/AIDS"),
    _choice("DIABETES", "Diabetes mellitus"),
    _choice("HYPERTENSION", "Hypertension"),
    _choice("HEART_DISEASE", "Heart disease"),
    _choice("RENAL_DISEASE", "Chronic kidney disease"),
    _choice("LIVER_DISEASE", "Liver disease"),
    _choice("MALNUTRITION", "Malnutrition"),
    _choice("OTHER", "Other"),
]

BREATHING_CHOICES = [
    _choice("NORMAL", "Normal"),
    _choice("MILD_DYSPNEA", "Mild dyspnoea"),
    _choice("MODERATE_DYSPNEA", "Moderate dyspnoea"),
    _choice("SEVERE_DYSPNEA", "Severe dyspnoea"),
]

VACCINATION_CHOICES = [
    _choice("BCG", "BCG"),
    _choice("COVID_19", "COVID-19 vaccine"),
    _choice("INFLUENZA", "Influenza vaccine"),
    _choice("PNEUMOCOCCAL", "Pneumococcal vaccine"),
    _choice("NONE", "None"),
]

COUGHING_STATUS_CHOICES = [
    _choice("YES", "Yes"),
    _choice("NO", "No"),
    _choice("RESOLVED", "Resolved"),
]

COUGH_TYPE_CHOICES = [
    _choice("DRY", "Dry"),
    _choice("PRODUCTIVE", "Productive"),
    _choice("MIXED", "Mixed"),
]

SPUTUM_PRODUCTION_CHOICES = [
    _choice("NONE", "None"),
    _choice("SCANTY", "Scanty"),
    _choice("MODERATE", "Moderate"),
    _choice("COPIOUS", "Copious"),
]

SPUTUM_COLOUR_CHOICES = [
    _choice("CLEAR", "Clear / White"),
    _choice("YELLOW", "Yellow"),
    _choice("GREEN", "Green"),
    _choice("BROWN", "Brown"),
    _choice("BLOOD_STAINED", "Blood-stained"),
]

SPUTUM_VOLUME_CHOICES = [
    _choice("LESS_THAN_10ML", "< 10 ml/day"),
    _choice("10_TO_30ML", "10–30 ml/day"),
    _choice("30_TO_100ML", "30–100 ml/day"),
    _choice("MORE_THAN_100ML", "> 100 ml/day"),
]

COUGH_FREQUENCY_CHOICES = [
    _choice("OCCASIONAL", "Occasional (< once/hour)"),
    _choice("FREQUENT", "Frequent (1–5 times/hour)"),
    _choice("VERY_FREQUENT", "Very frequent (> 5 times/hour)"),
    _choice("CONSTANT", "Constant"),
]

PRESENT_ABSENT_CHOICES = [
    _choice("PRESENT", "Present"),
    _choice("ABSENT", "Absent"),
]

TREATMENT_REGIMEN_CHOICES = [
    _choice("2HRZE_4HR", "2HRZE/4HR (Standard TB)"),
    _choice("2HRZE_4H3R3", "2HRZE/4H3R3"),
    _choice("DOTS", "DOTS"),
    _choice("INHALED_CORTICOSTEROID", "Inhaled corticosteroid"),
    _choice("SABA", "Short-acting beta-agonist (SABA)"),
    _choice("LABA_ICS", "LABA + ICS combination"),
    _choice("LAMA", "Long-acting muscarinic antagonist (LAMA)"),
    _choice("ANTIBIOTICS", "Antibiotics"),
    _choice("OTHER", "Other"),
]

DOSE_FREQUENCY_CHOICES = [
    _choice("ONCE_DAILY", "Once daily"),
    _choice("TWICE_DAILY", "Twice daily"),
    _choice("THREE_TIMES_DAILY", "Three times daily"),
    _choice("FOUR_TIMES_DAILY", "Four times daily"),
    _choice("AS_NEEDED", "As needed (PRN)"),
    _choice("WEEKLY", "Weekly"),
    _choice("OTHER", "Other"),
]

DOSE_DURATION_CHOICES = [
    _choice("LESS_THAN_1_WEEK", "< 1 week"),
    _choice("1_TO_4_WEEKS", "1–4 weeks"),
    _choice("1_TO_6_MONTHS", "1–6 months"),
    _choice("6_TO_12_MONTHS", "6–12 months"),
    _choice("MORE_THAN_1_YEAR", "> 1 year"),
    _choice("ONGOING", "Ongoing / Long-term"),
]

# Clinical medication choices
MEDICATION_CHOICES = [
    _choice("ISONIAZID", "Isoniazid (H)"),
    _choice("RIFAMPICIN", "Rifampicin (R)"),
    _choice("PYRAZINAMIDE", "Pyrazinamide (Z)"),
    _choice("ETHAMBUTOL", "Ethambutol (E)"),
    _choice("STREPTOMYCIN", "Streptomycin (S)"),
    _choice("SALBUTAMOL", "Salbutamol"),
    _choice("BUDESONIDE", "Budesonide"),
    _choice("FLUTICASONE", "Fluticasone"),
    _choice("TIOTROPIUM", "Tiotropium"),
    _choice("SALMETEROL_FLUTICASONE", "Salmeterol/Fluticasone"),
    _choice("PREDNISOLONE", "Prednisolone"),
    _choice("AMOXICILLIN", "Amoxicillin"),
    _choice("AZITHROMYCIN", "Azithromycin"),
    _choice("OTHER", "Other"),
]

# Cough recording choices
PATIENT_TYPE_CHOICES = [
    _choice("TB", "TB patient"),
    _choice("ASTHMA", "Asthma patient"),
    _choice("COPD", "COPD patient"),
    _choice("CONTROL", "Healthy control"),
    _choice("OTHER", "Other"),
]

TIMEPOINT_CHOICES = [
    _choice("BASELINE", "Baseline (start of treatment)"),
    _choice("WEEK_2", "Week 2"),
    _choice("MONTH_1", "Month 1"),
    _choice("MONTH_2", "Month 2"),
    _choice("END_OF_TREATMENT", "End of treatment"),
    _choice("FOLLOW_UP", "Follow-up"),
]

SETTING_CHOICES = [
    _choice("CLINIC", "Clinic / Hospital"),
    _choice("COMMUNITY", "Community"),
    _choice("HOME", "Home visit"),
]

RECORDING_LOCATION_CHOICES = [
    _choice("CONSULTATION_ROOM", "Consultation room"),
    _choice("WARD", "Hospital ward"),
    _choice("OUTDOOR", "Outdoor"),
    _choice("HOME", "Home"),
    _choice("OTHER", "Other"),
]

QC_STATUS_CHOICES = [
    _choice("PENDING", "Pending review"),
    _choice("PASS", "Pass"),
    _choice("FAIL", "Fail"),
    _choice("UNCERTAIN", "Uncertain"),
]

ALLOWED_AUDIO_EXTENSIONS = ["wav"]
DEFAULT_DEVICE_USED = "Android device (built-in microphone)"
