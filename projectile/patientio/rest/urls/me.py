from django.urls import path

from ..views.me import (
    PrivatePatientDetail,
    PrivateRelativePatientList,
    PrivateRelativePatientDetail,
    PrivatePatientSeekHelpList,
    PrivatePatientMedicineList,
)

urlpatterns = [
    path("/seek-helps", PrivatePatientSeekHelpList.as_view(), name="seek-help-list"),
    path(
        "/medicines", PrivatePatientMedicineList.as_view(), name="doctor-medicine-list"
    ),
    path(
        "/relatives/<uuid:uid>",
        PrivateRelativePatientDetail.as_view(),
        name="patient-relative-detail",
    ),
    path(
        "/relatives", PrivateRelativePatientList.as_view(), name="patient-relative-list"
    ),
    path("/<uuid:uid>", PrivatePatientDetail.as_view(), name="patient-detail"),
]
