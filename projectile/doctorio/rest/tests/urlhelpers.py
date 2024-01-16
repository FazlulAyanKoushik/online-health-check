from django.urls import reverse


def doctor_detail_url():
    return reverse("doctor-profile")


def doctor_reset_password_url():
    return reverse("doctor-reset-password")


def doctor_update_name_url():
    return reverse("doctor-update-name")


def doctor_appointment_list_url():
    return reverse("doctor-appointment-list")


def doctor_appointment_detail_url(uid):
    return reverse("doctor-appointment-detail", args=[uid])


def doctor_appointment_patient_list_url():
    return reverse("doctor-appointment-patient-list")


def doctor_appointment_patient_detail_url(uid):
    return reverse("doctor-appointment-patient-detail", args=[uid])
