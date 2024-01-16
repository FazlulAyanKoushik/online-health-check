from django.urls import reverse


def patient_appointment_list_url():
    return reverse("patient-appointment-list")


def patient_appointment_detail_url(uid):
    return reverse("patient-appointment-detail", args=[uid])


def prescription_list_url():
    return reverse("prescription-list")


def prescription_detail_url(prescription_uid):
    return reverse("prescription-detail", args=[prescription_uid])


def patient_appointment_refill_url(appointment_uid):
    return reverse("refill-list", args=[appointment_uid])


def patient_appointment_refill_detail_url(appointment_uid, uid):
    return reverse("refill-detail", args=[appointment_uid, uid])


def patient_detail_url(uid):
    return reverse("patient-detail", args=[uid])
