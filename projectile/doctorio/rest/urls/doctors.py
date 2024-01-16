from django.urls import path

from ..views import doctors


urlpatterns = [
    path(
        "/patients/<uuid:uid>",
        doctors.PrivateDoctorAppointmentPatientDetail.as_view(),
        name="doctor-appointment-patient-detail",
    ),
    path(
        "/patients",
        doctors.PrivateDoctorAppointmentPatientList.as_view(),
        name="doctor-appointment-patient-list",
    ),
    path(
        "/medicine/<uuid:uid>",
        doctors.PrivateDoctorMedicineDetail.as_view(),
        name="doctor-medicine-detail",
    ),
    path(
        "/medicine",
        doctors.PrivateDoctorMedicineList.as_view(),
        name="doctor-medicine-list",
    ),
    path(
        "/reset/password",
        doctors.PrivateDoctorResetPassword.as_view(),
        name="doctor-reset-password",
    ),
    path(
        "/update/name",
        doctors.PrivateDoctorUpdateName.as_view(),
        name="doctor-update-name",
    ),
    path("", doctors.PrivateMeDoctorDetail.as_view(), name="doctor-profile"),
]
