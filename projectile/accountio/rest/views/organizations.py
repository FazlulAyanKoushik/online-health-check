from rest_framework import generics
from rest_framework.generics import get_object_or_404

from drf_spectacular.utils import extend_schema

from accountio.models import Organization

from accountio.rest.serializers.organizations import (
    PublicOrganizationDoctorsSerializers,
    PublicOrganizationListSerializer,
)

from doctorio.models import Doctor

from doctorio.rest.permissions import IsOrganizationStaff


@extend_schema(
    responses=PublicOrganizationListSerializer,
)
class PublicOrganizationList(generics.ListAPIView):
    serializer_class = PublicOrganizationListSerializer
    queryset = Organization.objects.get_status_active()
    pagination_class = None
    permission_classes = []


class PublicOrganizationDoctorsList(generics.ListAPIView):
    queryset = Doctor.objects.get_status_editable()
    serializer_class = PublicOrganizationDoctorsSerializers
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = get_object_or_404(
            Organization.objects.filter(), slug=self.kwargs.get("organization_slug")
        )

        return self.queryset.filter(organization=organization)


class PublicOrganizationDoctorsDetail(generics.RetrieveAPIView):
    queryset = Doctor.objects.get_status_editable()
    serializer_class = PublicOrganizationDoctorsSerializers
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        organization = get_object_or_404(
            Organization.objects.filter(), slug=self.kwargs.get("organization_slug")
        )

        return get_object_or_404(
            self.queryset.filter(organization=organization),
            slug=self.kwargs.get("doctor_slug"),
        )
