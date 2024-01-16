from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)

from appointmentio.models import Refill
from doctorio.models import Department, Doctor
from doctorio.rest.permissions import IsOrganizationStaff

from weapi.rest.serializers.organizations import (
    PrivateOrganizationUserListSerializer,
    PrivateOrganizationDepartmentSerializer,
    PrivateRefillSerializer,
)


class PrivateOrganizationList(ListAPIView):
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateOrganizationUserListSerializer

    def get_queryset(self):
        return self.request.user.organizationuser_set.select_related(
            "organization"
        ).filter()


class PrivateOrganizationDepartmentList(ListCreateAPIView):
    queryset = Department.objects.filter()
    serializer_class = PrivateOrganizationDepartmentSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = self.request.user.get_organization()

        return self.queryset.prefetch_related("organization").filter(
            organization=organization
        )


class PrivateOrganizationDepartmentDetail(RetrieveAPIView):
    queryset = Department.objects.filter()
    serializer_class = PrivateOrganizationDepartmentSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}

        return get_object_or_404(
            self.queryset.prefetch_related("organization").filter(), **kwargs
        )


class PrivateOrganizationRefillList(ListAPIView):
    queryset = Refill.objects.all()
    serializer_class = PrivateRefillSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]


class PrivateOrganizationRefillDetail(RetrieveUpdateAPIView):
    queryset = Refill.objects.filter()
    serializer_class = PrivateRefillSerializer
    permission_classes = [IsOrganizationStaff]
    http_method_names = ["patch"]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("refill_uid", None)}

        return get_object_or_404(
            self.queryset.select_related("appointment", "patient").filter(), **kwargs
        )
