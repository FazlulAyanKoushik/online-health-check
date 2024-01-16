from datetime import datetime, date, timedelta

from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accountio.models import Organization

from appointmentio.choices import AppointmentStatus
from appointmentio.models import (
    Appointment,
    AppointmentSeekHelpConnector,
    AppointmentAllergicMedicationConnector,
    AppointmentMedicationConnector,
    WeekDay,
    Shift,
    AppointmentTimeSlot,
)

from common.slim_serializer import (
    PrivateSeekHelpSlimSerializer,
    PrivateAllergicMedicationSlimSerializer,
    PrivateCurrentMedicationSlimSerializer,
    PrivateMediaImageConnectorSlimSerializer,
    PrivateWeekDayWriteSlimSerializer,
)

from core.choices import UserType
from core.models import User

from doctorio.models import Doctor
from doctorio.rest.serializers.doctors import PublicDoctorSlimSerializer

from mediaroomio.models import MediaImageConnector

from patientio.models import Patient


class PrivateAppointmentPatientSlimSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    social_security_number = serializers.CharField(source="user.social_security_number")
    phone_number = serializers.CharField(source="user.phone")
    date_of_birth = serializers.CharField(source="user.date_of_birth")
    email = serializers.EmailField(source="user.email")
    weight = serializers.CharField(source="user.weight")
    height = serializers.CharField(source="user.height")
    nid = serializers.CharField(source="user.nid")
    gender = serializers.CharField(source="user.gender")
    blood_group = serializers.CharField(source="user.blood_group")

    class Meta:
        model = Patient
        fields = [
            "uid",
            "first_name",
            "last_name",
            "social_security_number",
            "phone_number",
            "nid",
            "gender",
            "blood_group",
            "date_of_birth",
            "email",
            "height",
            "weight",
            "image",
        ]
        read_only_fields = ["__all__"]


class PrivateAppointmentSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    doctor_uid = serializers.SlugRelatedField(
        queryset=Doctor.objects.get_status_editable(),
        slug_field="uid",
        write_only=True,
        allow_null=True,
        allow_empty=True,
        required=False,
    )
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    seek_help_list = serializers.SerializerMethodField(read_only=True)
    allergic_medication_list = serializers.SerializerMethodField(read_only=True)
    current_medication_list = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        user = self.context["request"].user
        doctor_uid: Doctor = data.get("doctor_uid", None)
        organization: Organization = user.get_organization()
        if doctor_uid and not organization.doctor_set.filter(pk=doctor_uid.pk).exists():
            raise ValidationError({"doctor_uid": "Invalid organization doctor."})

        return data

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "complication",
            "symptom_period",
            "status",
            "is_visible",
            "patient",
            "doctor",
            "schedule_start",
            "schedule_end",
            "doctor_uid",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone",
            "email",
            "weight",
            "height",
            "blood_group",
            "gender",
            "seek_help_list",
            "allergic_medication_list",
            "current_medication_list",
            "file_item_list",
        ]

        read_only_fields = ["serial_number"]

    def create(self, validated_data):
        request = self.context["request"]
        phone_number = validated_data.get("phone", None)
        first_name = validated_data.get("first_name", "")
        last_name = validated_data.get("last_name", "")
        date_of_birth = validated_data.get("date_of_birth", "")
        email = validated_data.get("email", "")
        gender = validated_data.get("gender", "")
        blood_group = validated_data.get("blood_group", "")
        height = validated_data.get("height", "")
        weight = validated_data.get("weight", "")
        organization: Organization = request.user.get_organization()

        # creating user if not found
        if phone_number:
            if User.objects.filter(phone=phone_number).exists():
                user = User.objects.get(phone=phone_number)
                existing_patient = Patient.objects.get(user=user)
                validated_data["first_name"] = existing_patient.user.first_name
                validated_data["last_name"] = existing_patient.user.last_name
                validated_data["date_of_birth"] = existing_patient.user.date_of_birth
                validated_data["email"] = existing_patient.user.email
                validated_data["gender"] = existing_patient.user.gender
                validated_data["blood_group"] = existing_patient.user.blood_group
                validated_data["height"] = existing_patient.user.height
                validated_data["weight"] = existing_patient.user.weight
            else:
                if email and User.objects.filter(email=email).exists():
                    raise ValidationError("This email already exists.")
                else:
                    user = User.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=date_of_birth,
                        phone=phone_number,
                        email=email,
                        gender=gender,
                        blood_group=blood_group,
                        height=height,
                        weight=weight,
                        username=phone_number,
                        type=UserType.PATIENT,
                    )
        else:
            user = request.user

        patient, _ = Patient.objects.get_or_create(user=user, organization=organization)
        validated_data["patient"] = patient
        validated_data["doctor"] = validated_data.pop("doctor_uid", None)
        validated_data["organization"] = organization
        validated_data["creator_user"] = request.user

        appointment = Appointment.objects.create(**validated_data)

        return appointment

    def update(self, instance, validated_data):
        request = self.context["request"]
        phone_number = validated_data.get("phone", None)
        first_name = validated_data.get("first_name", "")
        last_name = validated_data.get("last_name", "")
        date_of_birth = validated_data.get("date_of_birth", "")
        email = validated_data.get("email", "")
        gender = validated_data.get("gender", "")
        blood_group = validated_data.get("blood_group", "")
        height = validated_data.get("height", "")
        weight = validated_data.get("weight", "")
        status = validated_data.get("status", "")
        organization: Organization = request.user.get_organization()

        if phone_number:
            user, _ = User.objects.get_or_create(
                phone=phone_number,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": date_of_birth,
                    "email": email,
                    "gender": gender,
                    "blood_group": blood_group,
                    "height": height,
                    "weight": weight,
                    "username": phone_number,
                    "type": UserType.PATIENT,
                },
            )
        else:
            user = request.user

        validated_data["doctor"] = validated_data.get("doctor_uid", instance.doctor)
        validated_data["user"] = user
        validated_data["organization"] = organization

        if status and status == AppointmentStatus.COMPLETED:
            now = datetime.now()
            instance.schedule_end = now
            instance.save()

        return super().update(instance=instance, validated_data=validated_data)

    def get_seek_help_list(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        return PrivateSeekHelpSlimSerializer(seek_helps, many=True).data

    def get_allergic_medication_list(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_current_medication_list(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
        ).data

    def get_file_item_list(self, obj):
        file_items = MediaImageConnector.objects.filter(
            appointment=obj, patient=obj.patient
        )
        request = self.context.get("request")

        return PrivateMediaImageConnectorSlimSerializer(
            file_items, many=True, context={"request": request}
        ).data


class PrivateAppointmentScheduleCreateSerializer(serializers.Serializer):
    appointment_duration = serializers.TimeField(
        write_only=True, allow_null=True, required=False
    )
    appointment_interval = serializers.TimeField(
        write_only=True, allow_null=True, required=False
    )
    appointment_fee = serializers.FloatField(
        write_only=True, allow_null=True, required=False
    )
    consultation_fee = serializers.FloatField(
        write_only=True, allow_null=True, required=False
    )
    follow_up_fee = serializers.FloatField(
        write_only=True, allow_null=True, required=False
    )
    checkup_fee = serializers.FloatField(
        write_only=True, allow_null=True, required=False
    )
    week_day = PrivateWeekDayWriteSlimSerializer(
        write_only=True, many=True, allow_null=True, allow_empty=True, required=False
    )

    def create(self, validated_data):
        with transaction.atomic():
            appointment_duration = validated_data.pop("appointment_duration", None)
            appointment_interval = validated_data.pop("appointment_interval", None)
            appointment_fee = validated_data.pop("appointment_fee", 0)
            consultation_fee = validated_data.pop("consultation_fee", 0)
            follow_up_fee = validated_data.pop("follow_up_fee", 0)
            checkup_fee = validated_data.pop("checkup_fee", 0)
            week_days = validated_data.pop("week_day", [])
            organization = self.context["request"].user.get_organization()

            try:
                Doctor.objects.update(
                    appointment_duration=appointment_duration,
                    appointment_interval=appointment_interval,
                    appointment_fee=appointment_fee,
                    consultation_fee=consultation_fee,
                    follow_up_fee=follow_up_fee,
                    check_up_fee=checkup_fee,
                )

            except Doctor.DoesNotExist:
                raise ValidationError("Doctor doesn't exist!")

            time_slot_list = []

            # Before creating or updating Weekday, we first delete all Weekdays to avoid multiple creation of Weekday.
            # if we delete all weekday it will delete all related AppointmentTimeSlot models data.
            # That will help us to avoid multiple creation of AppointmentTimeSlot also.
            WeekDay.objects.filter(organization=organization).delete()

            for week_day in week_days:
                shift_list = []

                week_day_object = WeekDay.objects.create(
                    organization=organization,
                    day=week_day["day"],
                    off_day=week_day["off_day"],
                )

                if "shift" in week_day:
                    for shift in week_day["shift"]:
                        shift_list.append(
                            Shift(
                                weekday=week_day_object,
                                shift_label=shift["shift_label"],
                                start_time=shift["start_time"],
                                end_time=shift["end_time"],
                            )
                        )

                if shift_list:
                    shifts = Shift.objects.bulk_create(shift_list)

                    for per_shift in shifts:
                        start_time = per_shift.start_time
                        end_time = per_shift.end_time

                        while start_time < end_time:
                            schedule_time = datetime.combine(
                                date.today(), start_time.replace(minute=0)
                            )
                            time_slot_list.append(
                                AppointmentTimeSlot(
                                    organization=organization,
                                    weekday=week_day_object,
                                    schedule_time=schedule_time.strftime("%H:%M"),
                                    slot=start_time,
                                )
                            )
                            start_time = (
                                datetime.combine(date.today(), start_time)
                                + timedelta(
                                    minutes=appointment_duration.minute
                                    + appointment_interval.minute
                                )
                            ).time()

                else:
                    time_slot_list.append(
                        AppointmentTimeSlot(
                            organization=organization,
                            weekday=week_day_object,
                        )
                    )

            AppointmentTimeSlot.objects.bulk_create(time_slot_list)

            return validated_data
