from datetime import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accountio.models import (
    PrescriptionAdditionalConnector,
    Diagnosis,
    Investigation,
    Examination,
    Organization,
)
from appointmentio.choices import AppointmentStatus

from appointmentio.models import (
    Appointment,
    Prescription,
    PrescriptionInformation,
    PrescriptionMedicineConnector,
    AppointmentSeekHelpConnector,
    AppointmentAllergicMedicationConnector,
    AppointmentMedicationConnector,
    WeekDay,
    AppointmentTimeSlot,
    AppointmentDateTimeSlotConnector,
)

from common.slim_serializer import (
    PublicOrganizationSlimSerializer,
    PrivatePatientSlimSerializer,
    PrivateAppointmentPatientSlimSerializer,
    PrescriptionMedicineConnectorTreatmentSlimSerializer,
    RecommendationSlimSerializer,
    DiagnosisSlimSerializer,
    InvestigationSlimSerializer,
    ExaminationSlimSerializer,
    PrimaryDiseaseSlimSerializer,
    MedicineDoseSlimSerializer,
    PrivateSeekHelpSlimSerializer,
    PrivateAllergicMedicationSlimSerializer,
    PrivateCurrentMedicationSlimSerializer,
    PrivateMediaImageConnectorSlimSerializer,
)

from doctorio.models import Recommendations
from doctorio.rest.serializers.doctors import PublicDoctorSlimSerializer

from mediaroomio.models import MediaImageConnector

from patientio.models import PrimaryDisease


class PrivateDoctorAppointmentListSerializer(serializers.ModelSerializer):
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    doctor = PublicDoctorSlimSerializer(read_only=True)

    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
    )

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
            "first_name",
            "last_name",
            "weight",
            "height",
            "age",
            "gender",
            "blood_group",
            "symptom_period",
            "complication",
            "organization",
            "doctor",
            "patient",
            "allergic_medication_list",
            "current_medication_list",
            "schedule_start",
            "schedule_end",
            "file_item_list",
            "seek_help_list",
            "status",
        ]

        read_only_fields = ["__all__"]

    def get_current_medication_list(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
        ).data

    def get_allergic_medication_list(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_seek_help_list(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        return PrivateSeekHelpSlimSerializer(seek_helps, many=True).data

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


class PrivatePrescriptionRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["uid", "next_visit"]
        read_only_fields = ["__all__"]


class PrivateDoctorAppointmentDetailSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    prescriptions = serializers.SerializerMethodField(
        "get_prescriptions", read_only=True
    )
    patient = PrivatePatientSlimSerializer(read_only=True)
    seek_helps = serializers.SerializerMethodField(read_only=True)
    allergic_medication_list = serializers.SerializerMethodField(read_only=True)
    current_medication_list = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_type",
            "appointment_for",
            "first_name",
            "last_name",
            "weight",
            "height",
            "age",
            "gender",
            "blood_group",
            "complication",
            "symptom_period",
            "status",
            "is_visible",
            "patient",
            "doctor",
            "prescriptions",
            "organization",
            "allergic_medication_list",
            "current_medication_list",
            "schedule_start",
            "schedule_end",
            "created_at",
            "updated_at",
            "file_item_list",
            "seek_helps",
        ]

        read_only_fields = [
            "uid",
            "serial_number",
            "appointment_type",
            "appointment_for",
            "complication",
            "is_visible",
            "patient",
            "doctor",
            "prescriptions",
            "organization",
            "schedule_start",
            "schedule_end",
            "created_at",
            "updated_at",
            "gender",
            "blood_group",
            "file_item_list",
            "seek_helps",
        ]

    def get_prescriptions(self, instance):
        try:
            appointment_uid = self.context["view"].kwargs.get("appointment_uid")
            prescription = Prescription.objects.filter(
                appointment__uid=appointment_uid
            ).select_related("appointment", "patient", "doctor")
            return PrivatePrescriptionRelatedSerializer(
                instance=prescription, many=True
            ).data

        except:
            return {}

    def update(self, instance, validated_data):
        appointment_uid = self.context["view"].kwargs.get("appointment_uid")
        try:
            appointment = Appointment.objects.get(uid=appointment_uid)
            schedule_date = appointment.schedule_start.date()
            schedule_time = appointment.schedule_start.time()
        except Appointment.DoesNotExist:
            raise ValidationError("Appointment not found!")

        status = validated_data.get("status", "")

        if status and status == AppointmentStatus.COMPLETED:
            now = datetime.now()
            instance.status = status
            instance.schedule_end = now
            instance.save()

            day = schedule_date.strftime("%A").upper()

            try:
                weekday = WeekDay.objects.select_related("organization").get(
                    organization=appointment.organization, day=day, off_day=False
                )
                appointment_time_slot = AppointmentTimeSlot.objects.select_related(
                    "organization", "weekday"
                ).get(
                    organization=appointment.organization,
                    weekday=weekday,
                    slot=schedule_time,
                )
                date_time_slot_connector = (
                    AppointmentDateTimeSlotConnector.objects.select_related(
                        "organization", "appointment", "appointment_time_slot"
                    ).filter(
                        organization=appointment.organization,
                        appointment=appointment,
                        date=schedule_date,
                        appointment_time_slot=appointment_time_slot,
                    )
                )
            except AppointmentTimeSlot.DoesNotExist:
                raise ValidationError("Appointment schedule time doesn't exist!")

            date_time_slot_connector.update(is_booked=False)

        return instance

    def get_current_medication_list(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
        ).data

    def get_allergic_medication_list(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_seek_helps(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        return PrivateSeekHelpSlimSerializer(seek_helps, many=True).data

    def get_file_item_list(self, obj):
        file_items = MediaImageConnector.objects.filter(
            appointment=obj, patient=obj.patient
        )

        request = self.context.get("request")

        return PrivateMediaImageConnectorSlimSerializer(
            file_items, many=True, context={"request": request}
        ).data


class PrivateDoctorAppointmentPrescriptionSerializer(serializers.ModelSerializer):
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

    medicine_doses = MedicineDoseSlimSerializer(write_only=True, many=True)
    recommendation_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    diagnosis_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    investigation_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    examination_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    primary_disease_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    schedule_start = serializers.DateTimeField(
        source="appointment.schedule_start", read_only=True, default=""
    )
    schedule_end = serializers.DateTimeField(
        source="appointment.schedule_end", read_only=True, default=""
    )

    class Meta:
        model = Prescription
        fields = [
            "uid",
            "next_visit",
            "medicine_doses",
            "treatments",
            "recommendation_list",
            "diagnosis_list",
            "investigation_list",
            "examination_list",
            "primary_disease_list",
            "recommendations",
            "diagnoses",
            "investigations",
            "examinations",
            "primary_diseases",
            "schedule_start",
            "schedule_end",
        ]

    def create(self, validated_data):
        recommendation_list = validated_data.pop("recommendation_list", None)
        diagnosis_list = validated_data.pop("diagnosis_list", None)
        investigation_list = validated_data.pop("investigation_list", None)
        examination_list = validated_data.pop("examination_list", None)
        primary_disease_list = validated_data.pop("primary_disease_list", None)
        medicine_doses: MedicineDoseSlimSerializer = validated_data.pop(
            "medicine_doses"
        )

        recommendation_list = (
            recommendation_list.split("\n") if recommendation_list else None
        )
        diagnosis_list = diagnosis_list.split("\n") if diagnosis_list else None
        investigation_list = (
            investigation_list.split("\n") if investigation_list else None
        )
        examination_list = examination_list.split("\n") if examination_list else None
        primary_disease_list = (
            primary_disease_list.split("\n") if primary_disease_list else None
        )

        instance = super().create(validated_data)
        PrescriptionInformation.objects.create(
            prescription=instance, doctor=instance.doctor
        )
        for medicine in medicine_doses:
            prescription_medicine_connector = (
                PrescriptionMedicineConnector.objects.create(
                    prescription=instance,
                    medicine=medicine["medicine_uid"],
                    interval=medicine["interval"],
                    dosage=medicine["duration"],
                    frequency=medicine["indication"],
                )
            )
            PrescriptionAdditionalConnector.objects.create(
                prescription=instance,
                treatment=prescription_medicine_connector,
            )

        recommendations = []
        if recommendation_list:
            for recommendation_name in recommendation_list:
                recommendation, _ = Recommendations.objects.get_or_create(
                    name=recommendation_name
                )

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, recommendation=recommendation
                    )
                except:
                    recommendations.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, recommendation=recommendation
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(recommendations)

        diagnoses = []
        if diagnosis_list:
            for diagnosis_name in diagnosis_list:
                diagnosis, _ = Diagnosis.objects.get_or_create(name=diagnosis_name)

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, diagnosis=diagnosis
                    )
                except:
                    diagnoses.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, diagnosis=diagnosis
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(diagnoses)

        investigations = []
        if investigation_list:
            for investigation_name in investigation_list:
                investigation, _ = Investigation.objects.get_or_create(
                    name=investigation_name
                )

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, investigation=investigation
                    )
                except:
                    investigations.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, investigation=investigation
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(investigations)

        examinations = []
        if examination_list:
            for examination_name in examination_list:
                examination, _ = Examination.objects.get_or_create(
                    name=examination_name
                )

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, examination=examination
                    )
                except:
                    examinations.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, examination=examination
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(examinations)

        primary_diseases = []
        if primary_disease_list:
            for primary_disease_name in primary_disease_list:
                primary_disease, _ = PrimaryDisease.objects.get_or_create(
                    name=primary_disease_name
                )

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, primary_disease=primary_disease
                    )
                except:
                    primary_diseases.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, primary_disease=primary_disease
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(primary_diseases)

        return instance

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
