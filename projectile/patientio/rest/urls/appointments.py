from django.urls import path

from ..views.appointments import (
    PrivatePatientCompletedAppointmentList,
    PrivatePatientAppointmentList,
    PrivatePatientAppointmentDetail,
    PrivatePatientAppointmentPrescriptionList,
    PrivatePatientAppointmentPrescriptionDetail,
    PrivatePatientAppointmentRefillList,
    PrivatePatientAppointmentRefillDetail,
    PrivateAppointmentTimeSlotList,
)


urlpatterns = [
    path(
        "/<uuid:appointment_uid>/refill/<uuid:uid>",
        PrivatePatientAppointmentRefillDetail.as_view(),
        name="patient-appointment-refill-detail",
    ),
    path(
        "/<uuid:appointment_uid>/refill",
        PrivatePatientAppointmentRefillList.as_view(),
        name="patient-appointment-refill-list",
    ),
    path(
        "/<uuid:appointment_uid>/prescriptions/<uuid:uid>",
        PrivatePatientAppointmentPrescriptionDetail.as_view(),
        name="patient-appointment-prescription-detail",
    ),
    path(
        "/<uuid:appointment_uid>/prescriptions",
        PrivatePatientAppointmentPrescriptionList.as_view(),
        name="patient-appointment-prescription-list",
    ),
    path(
        "/<uuid:uid>",
        PrivatePatientAppointmentDetail.as_view(),
        name="patient-appointment-detail",
    ),
    path(
        "",
        PrivatePatientAppointmentList.as_view(),
        name="patient-appointment-list",
    ),
    path(
        "/complete",
        PrivatePatientCompletedAppointmentList.as_view(),
        name="patient-completed-appointment-list",
    ),
    path(
        "/time-slots",
        PrivateAppointmentTimeSlotList.as_view(),
        name="patient-appointment-slot-list",
    ),
]
