from django.urls import reverse


def user_token_login_url():
    return reverse("token_obtain_pair")


def we_detail_url():
    return reverse("we.detail")


def we_doctor_list_url():
    return reverse("we.doctor-list")


def we_doctor_detail_url(uid):
    return reverse("we.doctor-detail", args=[uid])


def we_user_detail_url():
    return reverse("we.get-user-detail")


def we_patient_list_url():
    return reverse("we.patient-list")


def we_patient_detail_url(patient_uid):
    return reverse("we.patient-detail", args=[patient_uid])


def we_patient_appointment_list_url(patient_uid):
    return reverse("we.patient-appointment-list", args=[patient_uid])


def we_patient_upcoming_appointment_list_url(patient_uid):
    return reverse("we.patient-upcoming-appointment-list", args=[patient_uid])


def we_patient_completed_appointment_list_url(patient_uid):
    return reverse("we.patient-completed-appointment-list", args=[patient_uid])


def we_appointment_list_url():
    return reverse("we.appointment-list")
