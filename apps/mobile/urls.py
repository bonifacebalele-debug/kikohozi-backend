from django.urls import path
from apps.mobile.views.auth import StatusView, LoginView, LogoutView, MeView
from apps.mobile.views.metadata import MetadataView
from apps.mobile.views.sync import (
    SyncParticipantView,
    SyncClinicalDataView,
    SyncClinicalMedicationsView,
    SyncCoughRecordingView,
)

urlpatterns = [
    path("status/", StatusView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", MeView.as_view()),
    path("metadata/", MetadataView.as_view()),
    path("sync/participant/", SyncParticipantView.as_view()),
    path("sync/clinical-data/", SyncClinicalDataView.as_view()),
    path("sync/clinical-medications/", SyncClinicalMedicationsView.as_view()),
    path("sync/cough-recording/", SyncCoughRecordingView.as_view()),
]
