from django.urls import reverse


def public_organization_list_url():
    return reverse("organization.list")


def public_organization_doctor_list_url(organization_slug):
    return reverse(
        "organization.doctor-list",
        kwargs={"organization_slug": organization_slug},
    )


def public_organization_doctor_detail_url(organization_slug, doctor_slug):
    return reverse(
        "organization.doctor-detail",
        kwargs={"organization_slug": organization_slug, "doctor_slug": doctor_slug},
    )
