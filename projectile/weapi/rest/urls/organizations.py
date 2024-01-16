from django.urls import path

from ..views.organizations import (
    PrivateOrganizationList,
    PrivateOrganizationDepartmentDetail,
    PrivateOrganizationDepartmentList,
    PrivateOrganizationRefillList,
    PrivateOrganizationRefillDetail,
)

urlpatterns = [
    path(
        "/departments/<uuid:uid>",
        PrivateOrganizationDepartmentDetail.as_view(),
        name="we.organization-department-detail",
    ),
    path(
        "/departments",
        PrivateOrganizationDepartmentList.as_view(),
        name="we.organization-department-list",
    ),
    path(
        "/refill/<uuid:refill_uid>",
        PrivateOrganizationRefillDetail.as_view(),
        name="we.organization-refill-detail",
    ),
    path(
        "/refill",
        PrivateOrganizationRefillList.as_view(),
        name="we.organization-refill-list",
    ),
    path("", PrivateOrganizationList.as_view(), name="we.organization-list"),
]
