from datetime import datetime

from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accountio.models import Organization

from appointmentio.models import (
    Appointment,
    AppointmentAllergicMedicationConnector,
    AppointmentMedicationConnector,
    AppointmentSeekHelpConnector,
    Medicine,
    Prescription,
    SeekHelp,
    Refill,
    WeekDay,
    AppointmentTimeSlot,
    AppointmentDateTimeSlotConnector,
)
from appointmentio.choices import AppointmentFor, AppointmentType, AppointmentStatus

from common.slim_serializer import (
    DiagnosisSlimSerializer,
    ExaminationSlimSerializer,
    InvestigationSlimSerializer,
    PrimaryDiseaseSlimSerializer,
    PublicOrganizationSlimSerializer,
    PublicDoctorSlimSerializer,
    PrivateSeekHelpSlimSerializer,
    PrivateAllergicMedicationSlimSerializer,
    PrivateCurrentMedicationSlimSerializer,
    PrivateMediaImageConnectorSlimSerializer,
    PrivateAppointmentPatientSlimSerializer,
    PrescriptionMedicineConnectorTreatmentSlimSerializer,
    PrivateAppointmentMedicationConnectorSlimSerializer,
    RecommendationSlimSerializer,
)

from mediaroomio.models import MediaImage, MediaImageConnector

from ...models import Patient, RelativePatient

from .prescriptions import PrivatePatientPrescriptionSerializer


class PrivatePatientAppointmentListSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    seek_helps = serializers.SerializerMethodField(read_only=True)
    allergic_medications = serializers.SerializerMethodField(read_only=True)
    current_medications = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)
    permission = serializers.BooleanField(default=False, required=False)

    appointment_date = serializers.CharField(write_only=True)
    appointment_time = serializers.CharField(write_only=True)
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
    )
    seek_help_list = serializers.ListField(
        child=serializers.CharField(),
        max_length=255,
        write_only=True,
        required=False,
    )
    allergic_medication_list = serializers.ListField(
        child=serializers.CharField(),
        max_length=255,
        write_only=True,
        required=False,
    )
    current_medication_list = PrivateAppointmentMedicationConnectorSlimSerializer(
        write_only=True, many=True, allow_empty=True, allow_null=True, required=False
    )
    file_items = serializers.ListField(write_only=True, required=False)
    seek_help_text = serializers.CharField(
        write_only=True,
        max_length=255,
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    parent_appointment = serializers.SlugRelatedField(
        queryset=Appointment.objects.all(),
        slug_field="uid",
        write_only=True,
        required=False,
        allow_empty=True,
        allow_null=True,
    )
    relative_patient = serializers.SlugRelatedField(
        queryset=RelativePatient.objects.all(),
        slug_field="uid",
        write_only=True,
        required=False,
        allow_empty=True,
        allow_null=True,
    )

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "first_name",
            "last_name",
            "weight",
            "height",
            "age",
            "gender",
            "blood_group",
            "relative_patient",
            "seek_help_list",
            "allergic_medication_list",
            "current_medication_list",
            "symptom_period",
            "complication",
            "permission",
            "appointment_date",
            "appointment_time",
            "organization",
            "file_items",
            "doctor",
            "patient",
            "seek_helps",
            "allergic_medications",
            "current_medications",
            "schedule_start",
            "schedule_end",
            "seek_help_text",
            "parent_appointment",
            "file_item_list",
            "status",
        ]

        read_only_fields = ["schedule_start", "schedule_end", "status"]

    def get_seek_helps(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        return PrivateSeekHelpSlimSerializer(seek_helps, many=True).data

    def get_allergic_medications(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_current_medications(self, obj):
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

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance["organization"] = PublicOrganizationSlimSerializer(
            Organization.objects.get(uid=instance["organization"])
        ).data
        return instance

    def create(self, validated_data):
        user = self.context["request"].user
        organization = validated_data.get("organization", None)
        appointment_for = validated_data.get("appointment_for", "")
        appointment_type = validated_data.get("appointment_type", "")
        first_name = validated_data.get("first_name", "")
        last_name = validated_data.get("last_name", "")
        weight = validated_data.get("weight", None)
        height = validated_data.get("height", None)
        age = validated_data.get("age", None)
        blood_group = validated_data.get("blood_group", "")

        parent_appointment = validated_data.pop("parent_appointment", None)
        relative_patient = validated_data.pop("relative_patient", None)
        file_items = validated_data.pop("file_items", [])
        seek_helps = validated_data.pop("seek_help_list", [])
        allergic_medicines = validated_data.pop("allergic_medication_list", [])
        current_medications = validated_data.pop("current_medication_list", [])
        permission = validated_data.pop("permission", None)
        appointment_date = validated_data.pop("appointment_date", None)
        appointment_time = validated_data.pop("appointment_time", None)
        seek_help_text = validated_data.pop("seek_help_text", "")

        date = datetime.strptime(appointment_date, "%Y-%m-%d")
        time = datetime.strptime(appointment_time, "%H:%M:%S").time()

        validated_data["schedule_start"] = datetime.combine(date, time)

        with transaction.atomic():
            try:
                patient = Patient.objects.select_related("user", "organization").get(
                    user=user, organization=organization
                )
            except Patient.DoesNotExist:
                raise ValidationError({"detail": "Patient not found!"})

            if appointment_for == AppointmentFor.ME:
                appointment = Appointment.objects.create(
                    patient=patient,
                    creator_user=user,
                    status=AppointmentStatus.REQUESTED,
                    **validated_data
                )
            else:
                if relative_patient is None:
                    relative_patient = RelativePatient.objects.create(
                        patient=patient,
                        first_name=first_name,
                        last_name=last_name,
                        height=height,
                        weight=weight,
                        age=age,
                        blood_group=blood_group,
                        # gender=gender
                    )

                appointment = Appointment.objects.create(
                    patient=patient,
                    creator_user=user,
                    relative_patient=relative_patient,
                    status=AppointmentStatus.REQUESTED,
                    **validated_data
                )

            if appointment_type == AppointmentType.FOLLOWUP:
                appointment.parent = parent_appointment
                appointment.doctor = parent_appointment.doctor
                appointment.status = AppointmentStatus.SCHEDULED
                appointment.save()

            seek_help_list = []
            for seek_help in seek_helps:
                try:
                    seek = SeekHelp.objects.get(name=seek_help)
                    seek_help_list.append(
                        AppointmentSeekHelpConnector(
                            appointment=appointment, seek_help=seek
                        )
                    )
                except SeekHelp.DoesNotExist:
                    raise ValidationError({"detail": "Seek help not found!"})

            AppointmentSeekHelpConnector.objects.bulk_create(seek_help_list)

            if seek_help_text:
                AppointmentSeekHelpConnector.objects.create(
                    appointment=appointment, seek_help_for=seek_help_text
                )

            allergic_medicines_list = []
            for allergic_medicine in allergic_medicines:
                medicine = Medicine.objects.filter(name=allergic_medicine)
                if medicine.exists():
                    allergic_medicines_list.append(
                        AppointmentAllergicMedicationConnector(
                            appointment=appointment, medicine=medicine.first()
                        )
                    )
                else:
                    allergic_medicines_list.append(
                        AppointmentAllergicMedicationConnector(
                            appointment=appointment, other_medicine=allergic_medicine
                        )
                    )
            AppointmentAllergicMedicationConnector.objects.bulk_create(
                allergic_medicines_list
            )

            current_medications_list = []
            for current_medication in current_medications:
                medicine = Medicine.objects.filter(name=current_medication["medicine"])
                if medicine.exists():
                    current_medications_list.append(
                        AppointmentMedicationConnector(
                            appointment=appointment,
                            medicine=medicine.first(),
                            usage=current_medication["usage"],
                        )
                    )
                else:
                    current_medications_list.append(
                        AppointmentMedicationConnector(
                            appointment=appointment,
                            other_medicine=current_medication["medicine"],
                            usage=current_medication["usage"],
                        )
                    )
            AppointmentMedicationConnector.objects.bulk_create(current_medications_list)

            if permission is True:
                try:
                    prescriptions = Prescription.objects.filter(patient=patient)
                    prescriptions.update(is_visible=True)
                except Prescription.DoesNotExist:
                    pass

            for file_item in file_items:
                try:
                    media_image = MediaImage.objects.get(uid=file_item["uid"])
                    media_image.caption = file_item["caption"]
                    media_image.save()
                    MediaImageConnector.objects.create(
                        image=media_image,
                        patient=patient,
                        appointment=appointment,
                        organization=organization,
                    )
                except MediaImage.DoesNotExist:
                    raise ValidationError({"detail": "Image not found!"})

            appointment.save()

            day = date.strftime("%A").upper()

            try:
                weekday = WeekDay.objects.select_related("organization").get(
                    organization=organization, day=day, off_day=False
                )
            except WeekDay.DoesNotExist:
                raise ValidationError("Off Day!")

            try:
                appointment_time_slot = AppointmentTimeSlot.objects.select_related(
                    "organization", "weekday"
                ).get(organization=organization, weekday=weekday, slot=time)
            except AppointmentTimeSlot.DoesNotExist:
                raise ValidationError("Appointment schedule time doesn't exist!")

            AppointmentDateTimeSlotConnector.objects.create(
                organization=organization,
                appointment=appointment,
                date=date,
                appointment_time_slot=appointment_time_slot,
            )

            return appointment


class PrivatePatientAppointmentDetailSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    seek_helps = serializers.SerializerMethodField(read_only=True)
    allergic_medications = serializers.SerializerMethodField(read_only=True)
    current_medications = serializers.SerializerMethodField(read_only=True)
    permission = serializers.BooleanField(default=False, required=False)
    file_item_list = serializers.SerializerMethodField(read_only=True)
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
    )
    recent_prescription = serializers.SerializerMethodField(
        read_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "first_name",
            "last_name",
            "weight",
            "height",
            "age",
            "gender",
            "blood_group",
            "symptom_period",
            "complication",
            "permission",
            "organization",
            "doctor",
            "patient",
            "allergic_medications",
            "current_medications",
            "seek_helps",
            "schedule_start",
            "schedule_end",
            "file_item_list",
            "status",
            "recent_prescription",
        ]

        read_only_fields = ["__all__"]

    def get_seek_helps(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        return PrivateSeekHelpSlimSerializer(seek_helps, many=True).data

    def get_allergic_medications(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_current_medications(self, obj):
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

    def get_recent_prescription(self, obj):
        patient = obj.patient
        recent_prescription = (
            Prescription.objects.filter(patient=patient, appointment=obj)
            .order_by("-created_at")
            .first()
        )
        serializer = PrivatePatientPrescriptionSerializer(
            recent_prescription, context=self.context
        )
        data = serializer.data

        if data.get("doctor"):
            doctor_data = data.get("doctor")
            if doctor_data and "image" in doctor_data:
                request = self.context.get("request")
            image_url = doctor_data.get("image")

            if image_url:
                doctor_data["image"] = request.build_absolute_uri(image_url)
        return data

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance["organization"] = PublicOrganizationSlimSerializer(
            Organization.objects.get(uid=instance["organization"])
        ).data
        return instance


class PrivateAppointmentPrescriptionSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    treatments = PrescriptionMedicineConnectorTreatmentSlimSerializer(
        read_only=True, source="prescriptionmedicineconnector_set", many=True
    )
    recommendations = RecommendationSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    diagnoses = DiagnosisSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    investigations = InvestigationSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    examinations = ExaminationSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    primary_diseases = PrimaryDiseaseSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    schedule_start = serializers.DateTimeField(
        source="appointment.schedule_start", read_only=True
    )

    class Meta:
        model = Prescription
        fields = [
            "uid",
            "doctor",
            "treatments",
            "recommendations",
            "diagnoses",
            "investigations",
            "examinations",
            "primary_diseases",
            "schedule_start",
        ]

        read_only_fields = ["__all__"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["recommendations"] = "\n".join(
            recommendation["name"]
            for recommendation in data["recommendations"]
            if recommendation
        )
        data["diagnoses"] = "\n".join(
            diagnosis["name"] for diagnosis in data["diagnoses"] if diagnosis
        )
        data["investigations"] = "\n".join(
            investigation["name"]
            for investigation in data["investigations"]
            if investigation
        )
        data["examinations"] = "\n".join(
            examination["name"] for examination in data["examinations"] if examination
        )
        data["primary_diseases"] = "\n".join(
            primary_disease["name"]
            for primary_disease in data["primary_diseases"]
            if primary_disease
        )
        return data


class PrivatePatientAppointmentRefillSerializer(serializers.ModelSerializer):
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    appointment = PrivatePatientAppointmentDetailSerializer(read_only=True)

    class Meta:
        model = Refill
        fields = [
            "uid",
            "serial_number",
            "appointment",
            "message",
            "patient",
            "status",
        ]
        read_only_fields = ["uid", "serial_number", "status", "patient"]

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            patient = Patient.objects.select_related("user").get(user=user)
        except Patient.DoesNotExist:
            raise ValidationError({"detail": "Patient not found!"})

        return Refill.objects.create(patient=patient, **validated_data)
