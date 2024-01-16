from django.urls import path

from ..views.patient import (
    PrivateOrganizationPatientList,
    PrivateOrganizationPatientDetail,
    PrivateOrganizationPatientUpcomingAppointmentList,
    PrivateOrganizationPatientCompletedAppointmentList,
    PrivateOrganizationPatientAppointmentList,
)

urlpatterns = [
    path(
        "/<uuid:patient_uid>/appointments/completed",
        PrivateOrganizationPatientCompletedAppointmentList.as_view(),
        name="we.patient-completed-appointment-list",
    ),
    path(
        "/<uuid:patient_uid>/appointments/upcoming",
        PrivateOrganizationPatientUpcomingAppointmentList.as_view(),
        name="we.patient-upcoming-appointment-list",
    ),
    path(
        "/<uuid:patient_uid>/appointments",
        PrivateOrganizationPatientAppointmentList.as_view(),
        name="we.patient-appointment-list",
    ),
    path(
        "/<uuid:patient_uid>",
        PrivateOrganizationPatientDetail.as_view(),
        name="we.patient-detail",
    ),
    path("", PrivateOrganizationPatientList.as_view(), name="we.patient-list"),
]
