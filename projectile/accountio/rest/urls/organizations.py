from django.urls import path

from ..views import organizations

urlpatterns = [
    path(
        "/<slug:organization_slug>/doctors/<slug:doctor_slug>",
        organizations.PublicOrganizationDoctorsDetail.as_view(),
        name="organization.doctor-detail",
    ),
    path(
        "/<slug:organization_slug>/doctors",
        organizations.PublicOrganizationDoctorsList.as_view(),
        name="organization.doctor-list",
    ),
    path("", organizations.PublicOrganizationList.as_view(), name="organization.list"),
]
