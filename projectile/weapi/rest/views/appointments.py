from datetime import timedelta, datetime

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from appointmentio.choices import AppointmentStatus
from appointmentio.models import Appointment, AppointmentTimeSlot

from doctorio.rest.permissions import IsOrganizationStaff

from ..serializers.appointments import (
    PrivateAppointmentSerializer,
    PrivateAppointmentScheduleCreateSerializer,
)


class PrivateAppointmentList(generics.ListCreateAPIView):
    serializer_class = PrivateAppointmentSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "serial_number",
        "doctor__name",
        "patient__user__first_name",
        "patient__user__last_name",
    ]
    filterset_fields = {
        "status": ["exact"],
        "schedule_start": ["date"],
    }

    def get_queryset(self):
        last_week = self.request.query_params.get("last_weak", "")
        last_month = self.request.query_params.get("last_month", "")

        appointments: Appointment = (
            self.request.user.get_organization()
            .appointment_set.select_related("doctor", "patient")
            .filter()
        )

        # Calculated last week and last month dates
        today = timezone.now().date()

        if last_week:
            last_week = today - timedelta(days=7)
            last_week_start = timezone.make_aware(
                datetime.combine(last_week, datetime.min.time())
            )
            last_week_end = timezone.make_aware(
                datetime.combine(today, datetime.max.time())
            )
            appointments = appointments.filter(
                schedule_start__gte=last_week_start,
                schedule_start__lte=last_week_end,
                status=AppointmentStatus.COMPLETED,
            )

        if last_month:
            last_month = today - timedelta(days=30)
            last_month_start = timezone.make_aware(
                datetime.combine(last_month, datetime.min.time())
            )
            last_month_end = timezone.make_aware(
                datetime.combine(today, datetime.max.time())
            )
            appointments = appointments.filter(
                schedule_start__gte=last_month_start,
                schedule_start__lte=last_month_end,
                status=AppointmentStatus.COMPLETED,
            )

        return appointments


class PrivateAppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateAppointmentSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        uid = self.kwargs.get("uid", None)

        return get_object_or_404(
            self.request.user.get_organization()
            .appointment_set.select_related("doctor", "patient")
            .filter(),
            uid=uid,
        )

    def perform_destroy(self, instance):
        instance.status = AppointmentStatus.REMOVED
        instance.save()


class PrivateAppointmentScheduleCreate(APIView):
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateAppointmentScheduleCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PrivateAppointmentTimeSlotList(APIView):
    permission_classes = [IsOrganizationStaff]

    def get(self, request):
        organization = self.request.user.get_organization()
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
