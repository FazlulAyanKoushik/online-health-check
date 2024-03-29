from datetime import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from appointmentio.choices import AppointmentStatus
from appointmentio.models import (
    Appointment,
    Prescription,
    Refill,
    AppointmentTimeSlot,
)

from patientio.models import Patient

from ..permissions import IsPatient

from ..serializers.appointments import (
    PrivatePatientAppointmentListSerializer,
    PrivatePatientAppointmentDetailSerializer,
    PrivateAppointmentPrescriptionSerializer,
    PrivatePatientAppointmentRefillSerializer,
)


class PrivatePatientAppointmentList(ListCreateAPIView):
    serializer_class = PrivatePatientAppointmentListSerializer
    permission_classes = [IsPatient]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        "serial_number",
        "doctor__name",
    ]
    ordering_fields = ["created_at"]
    filterset_fields = ["status"]

    def get_queryset(self):
        patient = get_object_or_404(
            Patient.objects.select_related("user").filter(), user=self.request.user
        )
        return Appointment.objects.select_related("patient").filter(patient=patient)


class PrivatePatientAppointmentDetail(RetrieveAPIView):
    queryset = Appointment.objects.select_related("patient", "doctor").filter()
    serializer_class = PrivatePatientAppointmentDetailSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        patient = get_object_or_404(
            Patient.objects.select_related("user").filter(), user=self.request.user
        )
        kwargs = {"uid": self.kwargs.get("uid", None), "patient": patient}
        return get_object_or_404(self.queryset.filter(), **kwargs)


class PrivatePatientAppointmentPrescriptionList(ListAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrivateAppointmentPrescriptionSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        appointment = get_object_or_404(
            Appointment.objects.filter(), uid=self.kwargs.get("appointment_uid", None)
        )

        patient = get_object_or_404(
            Patient.objects.select_related("user").filter(), user=self.request.user
        )
        prescriptions = Prescription.objects.filter(
            patient=patient, appointment=appointment
        ).select_related("patient", "appointment")

        return prescriptions


class PrivatePatientAppointmentPrescriptionDetail(RetrieveAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrivateAppointmentPrescriptionSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        patient = get_object_or_404(
            Patient.objects.select_related("user").filter(), user=self.request.user
        )
        appointment = get_object_or_404(
            Appointment.objects.filter(), uid=self.kwargs.get("appointment_uid", None)
        )

        kwargs = {
            "uid": self.kwargs.get("uid", None),
            "patient": patient,
            "appointment": appointment,
        }

        prescription = get_object_or_404(
            Prescription.objects.filter().select_related("patient", "appointment"),
            **kwargs
        )

        return prescription


class PrivatePatientAppointmentRefillList(ListCreateAPIView):
    queryset = Refill.objects.select_related("patient", "appointment").filter()
    serializer_class = PrivatePatientAppointmentRefillSerializer
    permission_classes = [IsPatient]

    def perform_create(self, serializer):
        kwargs = {
            "uid": self.kwargs.get("appointment_uid", None),
        }
        appointment = get_object_or_404(Appointment.objects.filter(), **kwargs)
        serializer.save(appointment=appointment)


class PrivatePatientAppointmentRefillDetail(RetrieveUpdateAPIView):
    queryset = Refill.objects.select_related("patient", "appointment").filter()
    serializer_class = PrivatePatientAppointmentRefillSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        appointment = get_object_or_404(
            Appointment.objects.filter(), uid=self.kwargs.get("appointment_uid", None)
        )
        kwargs = {
            "uid": self.kwargs.get("uid", None),
            "appointment": appointment,
        }

        refill = get_object_or_404(self.queryset.filter(), **kwargs)

        return refill


class PrivateAppointmentTimeSlotList(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        organization = Patient.objects.get(user=self.request.user).organization
        date = request.query_params.get("date")
        if not date:
            return Response(
                "Date parameter is required.", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                "Invalid date format. Expected format: YYYY-MM-DD.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        day = date.strftime("%A").upper()

        appointment_time_slots = AppointmentTimeSlot.objects.filter(
            organization=organization, weekday__off_day=False, weekday__day=day
        ).prefetch_related("appointmentdatetimeslotconnector_set")

        appointment_slots = {}
        for slot in appointment_time_slots:
            appointment_slot_data = {
                "weekday": slot.weekday.day,
                "slot": datetime.strptime(str(slot.slot), "%H:%M:%S").strftime("%H:%M"),
                "is_booked": False,
                "date": date.strftime("%Y-%m-%d"),
            }

            # Check if the appointment slot is booked
            appointment = next(
                (
                    booked
                    for booked in slot.appointmentdatetimeslotconnector_set.all()
                    if booked.date == date and booked.is_booked == True
                ),
                None,
            )
            if appointment:
                appointment_slot_data["is_booked"] = appointment.is_booked

            schedule_time = slot.schedule_time.strftime("%H:%M")
            if schedule_time not in appointment_slots:
                appointment_slots[schedule_time] = []
            appointment_slots[schedule_time].append(appointment_slot_data)

        return Response(appointment_slots, status=status.HTTP_200_OK)


class PrivatePatientCompletedAppointmentList(ListAPIView):
    serializer_class = PrivatePatientAppointmentListSerializer
    permission_classes = [IsPatient]
    filter_backends = [filters.SearchFilter]
    search_fields = ["doctor__name"]

    def get_queryset(self):
        patient = get_object_or_404(
            Patient.objects.select_related("user").filter(), user=self.request.user
        )

        return (
            Appointment.objects.select_related("patient")
            .filter(patient=patient, status=AppointmentStatus.COMPLETED)
            .order_by("doctor__name")
        )
