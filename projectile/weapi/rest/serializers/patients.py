from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from versatileimagefield.serializers import VersatileImageFieldSerializer

from appointmentio.choices import AppointmentStatus
from appointmentio.models import (
    Appointment,
    AppointmentSeekHelpConnector,
    AppointmentAllergicMedicationConnector,
    AppointmentMedicationConnector,
)

from core.choices import UserType

from common.slim_serializer import (
    UserSlimSerializer,
    PublicDoctorSlimSerializer,
    PrivateSeekHelpSlimSerializer,
    PrivateAllergicMedicationSlimSerializer,
    PrivateCurrentMedicationSlimSerializer,
    PrivateMediaImageConnectorSlimSerializer,
)
from mediaroomio.models import MediaImageConnector

from patientio.models import Patient

User = get_user_model()


class PrivateOrganizationPatientListSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)
    first_name = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    last_name = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    phone = serializers.CharField(write_only=True)
    email = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    social_security_number = serializers.CharField(
        write_only=True,
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    date_of_birth = serializers.DateField(
        write_only=True,
        allow_null=True,
        required=False,
    )
    blood_group = serializers.CharField(
        write_only=True,
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    height = serializers.FloatField(write_only=True, allow_null=True, required=False)
    weight = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    gender = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    image = VersatileImageFieldSerializer(
        allow_null=True,
        allow_empty_file=True,
        required=False,
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
    )
    password = serializers.CharField(write_only=True)
    total_appointments = serializers.IntegerField(read_only=True)
    past_appointments = serializers.IntegerField(read_only=True)
    upcoming_appointment_date = serializers.SerializerMethodField(
        "get_upcoming_appointment_date", read_only=True
    )
    user = UserSlimSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "uid",
            "first_name",
            "last_name",
            "phone",
            "email",
            "social_security_number",
            "date_of_birth",
            "blood_group",
            "height",
            "weight",
            "gender",
            "image",
            "password",
            "total_appointments",
            "past_appointments",
            "upcoming_appointment_date",
            "user",
        ]

    def get_upcoming_appointment_date(self, instance):
        try:
            now = timezone.now()
            upcoming_appointment_date = Appointment.objects.filter(
                patient=instance,
                schedule_start__gt=now,
                status__in=[
                    AppointmentStatus.REQUESTED,
                    AppointmentStatus.PENDING,
                    AppointmentStatus.SCHEDULED,
                ],
            ).last()

            if upcoming_appointment_date:
                upcoming_appointment_date = (
                    upcoming_appointment_date.schedule_start.date()
                )

            else:
                upcoming_appointment_date = ""

            return upcoming_appointment_date

        except Appointment.DoesNotExist:
            return ""

    def validate_phone(self, value):
        if value and User.objects.filter(phone=value).exists():
            raise ValidationError("This phone number is already exists.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise ValidationError("This email address is already exists.")
        return value

    def validate_social_security_number(self, value):
        if value and User.objects.filter(social_security_number=value).exists():
            raise ValidationError("This social security number is already exists.")
        return value

    def create(self, validated_data):
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        phone = validated_data.pop("phone", None)
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)
        social_security_number = validated_data.pop("social_security_number", None)
        date_of_birth = validated_data.pop("date_of_birth", None)
        blood_group = validated_data.pop("blood_group", None)
        height = validated_data.pop("height", None)
        weight = validated_data.pop("weight", None)
        gender = validated_data.pop("gender", None)
        image = validated_data.pop("image", None)

        user, _ = User.objects.get_or_create(
            phone=phone,
            defaults={
                "username": phone,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "date_of_birth": date_of_birth,
                "blood_group": blood_group,
                "height": height,
                "weight": weight,
                "gender": gender,
                "social_security_number": social_security_number,
                "type": UserType.PATIENT,
            },
        )
        user.set_password(password)
        user.save()

        return Patient.objects.create(
            user=user,
            organization=self.context["request"].user.get_organization(),
            image=image,
        )


class PrivateOrganizationPatientDetailSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone = serializers.CharField(source="user.phone", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    date_of_birth = serializers.CharField(source="user.date_of_birth", read_only=True)
    social_security_number = serializers.CharField(
        source="user.social_security_number", read_only=True
    )
    blood_group = serializers.CharField(source="user.blood_group", read_only=True)
    height = serializers.CharField(source="user.height")
    weight = serializers.CharField(source="user.weight")
    gender = serializers.CharField(source="user.gender")
    image = serializers.CharField(source="user.image", read_only=True)
    total_appointments = serializers.IntegerField(read_only=True)
    past_appointments = serializers.IntegerField(read_only=True)
    upcoming_appointment_date = serializers.SerializerMethodField(
        "get_upcoming_appointment_date", read_only=True
    )
    user = UserSlimSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "uid",
            "first_name",
            "last_name",
            "phone",
            "email",
            "date_of_birth",
            "social_security_number",
            "blood_group",
            "height",
            "weight",
            "gender",
            "image",
            "total_appointments",
            "past_appointments",
            "upcoming_appointment_date",
            "user",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.get("user", {})
        instance.user.first_name = user_data.get("first_name", instance.user.first_name)
        instance.user.last_name = user_data.get("last_name", instance.user.last_name)
        instance.user.height = user_data.get("height", instance.user.height)
        instance.user.weight = user_data.get("weight", instance.user.weight)
        instance.user.gender = user_data.get("gender", instance.user.gender)

        instance.user.save()

        return instance

    def get_upcoming_appointment_date(self, instance):
        try:
            now = timezone.now()
            upcoming_appointment_date = Appointment.objects.filter(
                patient=instance,
                schedule_start__gt=now,
                status=AppointmentStatus.REQUESTED,
            ).last()

            if upcoming_appointment_date:
                upcoming_appointment_date = (
                    upcoming_appointment_date.schedule_start.date()
                )
            else:
                upcoming_appointment_date = ""

            return upcoming_appointment_date
        except Appointment.DoesNotExist:
            return ""


class PrivateOrganizationPatientAppointmentListSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    seek_help_list = serializers.SerializerMethodField(read_only=True)
    allergic_medication_list = serializers.SerializerMethodField(read_only=True)
    current_medication_list = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "complication",
            "status",
            "is_visible",
            "doctor",
            "schedule_start",
            "schedule_end",
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
        read_only_fields = ["__all__"]

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
