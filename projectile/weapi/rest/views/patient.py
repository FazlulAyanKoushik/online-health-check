from django.db.models import Count, Q
from django.utils import timezone

from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)

from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend

from appointmentio.choices import AppointmentStatus
from appointmentio.models import Appointment

from doctorio.rest.permissions import IsOrganizationStaff

from patientio.models import Patient

from ..serializers.patients import (
    PrivateOrganizationPatientListSerializer,
    PrivateOrganizationPatientDetailSerializer,
    PrivateOrganizationPatientAppointmentListSerializer,
)


class PrivateOrganizationPatientList(ListCreateAPIView):
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateOrganizationPatientListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "user__phone",
        "user__first_name",
        "user__last_name",
        "serial_number",
    ]
    filterset_fields = ("status",)

    def get_queryset(self):
        return (
            Patient.objects.filter(organization=self.request.user.get_organization())
            .annotate(
                total_appointments=Count("appointment"),
                past_appointments=Count(
                    "appointment",
                    filter=Q(
                        appointment__schedule_end__lt=timezone.now(),
                        appointment__status=AppointmentStatus.COMPLETED,
                    ),
                ),
            )
            .order_by("-created_at")
        )


class PrivateOrganizationPatientDetail(RetrieveUpdateAPIView):
    serializer_class = PrivateOrganizationPatientDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("patient_uid", None)}
        return get_object_or_404(
            Patient.objects.filter(organization=self.request.user.get_organization()),
            **kwargs
        )


class PrivateOrganizationPatientUpcomingAppointmentList(ListAPIView):
    queryset = Appointment.objects.get_status_upcoming()
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateOrganizationPatientAppointmentListSerializer

    def get_queryset(self):
        try:
            patient_uid = self.kwargs.get("patient_uid", None)
            patient = Patient.objects.get(uid=patient_uid)
        except Patient.DoesNotExist:
            raise ValidationError({"detail": "Patient not found."})
        queryset = self.queryset.filter(patient=patient)

        return queryset


class PrivateOrganizationPatientCompletedAppointmentList(ListAPIView):
    queryset = Appointment.objects.filter()
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateOrganizationPatientAppointmentListSerializer

    def get_queryset(self):
        try:
            patient_uid = self.kwargs.get("patient_uid", None)
            patient = Patient.objects.get(uid=patient_uid)
        except Patient.DoesNotExist:
            raise ValidationError({"detail": "Patient not found."})
        queryset = self.queryset.filter(
            patient=patient, status=AppointmentStatus.COMPLETED
        )

        return queryset


class PrivateOrganizationPatientAppointmentList(ListAPIView):
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateOrganizationPatientAppointmentListSerializer

    def get_queryset(self):
        try:
            patient_uid = self.kwargs.get("patient_uid", None)
            patient = Patient.objects.get(uid=patient_uid)

        except Patient.DoesNotExist:
            raise ValidationError({"detail": "Patient not found."})

        return Appointment.objects.filter(patient=patient)
