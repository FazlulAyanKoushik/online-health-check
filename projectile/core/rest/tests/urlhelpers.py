from django.urls import reverse


def me_detail_url():
    return reverse("me.detail")


def user_patient_url():
    return reverse("patient-register")
