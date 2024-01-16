from django.urls import path

from ..views.doctors import (
    PrivateDoctorAppointmentPrescriptionDetail,
    PrivateDoctorAppointmentPrescriptionList,
    PrivateDoctorAppointmentDetail,
    PrivateDoctorAppointmentList,
    PrivateDoctorAffiliationDetail,
    PrivateDoctorAffiliationList,
    PrivateDoctorExpertiseList,
    PrivateDoctorDetail,
    PrivateDoctorList,
    PrivateDoctorDegreeList,
    PrivateDoctorDegreeDetail,
    PrivateDoctorExpertiseDetail,
)

urlpatterns = [
    path(
        "/<uuid:doctor_uid>/appointments/<uuid:appointment_uid>/prescriptions/<uuid:uid>",
        PrivateDoctorAppointmentPrescriptionDetail.as_view(),
        name="we.appointment.prescription-detail",
    ),
    path(
        "/<uuid:doctor_uid>/appointments/<uuid:appointment_uid>/prescriptions",
        PrivateDoctorAppointmentPrescriptionList.as_view(),
        name="we.appointment.prescription-list",
    ),
    path(
        "/<uuid:doctor_uid>/appointments/<uuid:appointment_uid>",
        PrivateDoctorAppointmentDetail.as_view(),
        name="we.doctor.appointment-detail",
    ),
    path(
        "/<uuid:uid>/appointments",
        PrivateDoctorAppointmentList.as_view(),
        name="we.doctor-appointments-list",
    ),
    path(
        "/<uuid:doctor_uid>/affiliations/<uuid:uid>",
        PrivateDoctorAffiliationDetail.as_view(),
        name="we.doctor-affiliation-detail",
    ),
    path(
        "/<uuid:doctor_uid>/affiliations",
        PrivateDoctorAffiliationList.as_view(),
        name="we.doctor-affiliation-list",
    ),
    path(
        "/<uuid:doctor_uid>/expertises",
        PrivateDoctorExpertiseList.as_view(),
        name="we.doctor-expertises",
    ),
    path(
        "/<uuid:doctor_uid>/expertises/<uuid:uid>",
        PrivateDoctorExpertiseDetail.as_view(),
        name="doctor-expertise-detail",
    ),
    path(
        "/<uuid:doctor_uid>/degrees/<uuid:uid>",
        PrivateDoctorDegreeDetail.as_view(),
        name="we.doctor.degree-detail",
    ),
    path(
        "/<uuid:doctor_uid>/degrees",
        PrivateDoctorDegreeList.as_view(),
        name="we.doctor.degree-List",
    ),
    path("/<uuid:uid>", PrivateDoctorDetail.as_view(), name="we.doctor-detail"),
    path("", PrivateDoctorList.as_view(), name="we.doctor-list"),
]
