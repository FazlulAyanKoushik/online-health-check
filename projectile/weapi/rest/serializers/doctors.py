from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accountio.models import Affiliation, Organization
from accountio.choices import AffiliationStatus

from appointmentio.models import (
    Appointment,
    Prescription,
    AppointmentSeekHelpConnector,
    AppointmentAllergicMedicationConnector,
    AppointmentMedicationConnector,
)
from appointmentio.choices import AppointmentStatus

from core.choices import UserType
from common.slim_serializer import (
    PublicOrganizationSlimSerializer,
    PrivateAchievementSlimWriteSerializer,
    PrivateAchievementSlimReadSerializer,
    PrivateAffiliationSlimWriteSerializer,
    PrivateAffiliationSlimReadSerializer,
    PrivateDegreeSlimWriteSerializer,
    PrivateDegreeSlimReadSerializer,
    PrivateExpertiseSlimWriteSerializer,
    PrivateExpertiseSlimReadSerializer,
    PrescriptionMedicineConnectorTreatmentSlimSerializer,
    RecommendationSlimSerializer,
    DiagnosisSlimSerializer,
    InvestigationSlimSerializer,
    ExaminationSlimSerializer,
    PrimaryDiseaseSlimSerializer,
    PrivateOrganizationSlimSerializer,
    PrivateDepartmentSlimSerializer,
    PrivateAppointmentPatientSlimSerializer,
    PublicDoctorSlimSerializer,
    PrivateSeekHelpSlimSerializer,
    PrivateAllergicMedicationSlimSerializer,
    PrivateCurrentMedicationSlimSerializer,
    PrivateMediaImageConnectorSlimSerializer,
)

from doctorio.models import (
    Achievement,
    Department,
    DoctorAdditionalConnector,
    Degree,
    Doctor,
    Expertise,
)

from mediaroomio.models import MediaImageConnector

from versatileimagefield.serializers import VersatileImageFieldSerializer

User = get_user_model()


class PrivateDoctorSerializer(serializers.ModelSerializer):
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
    first_name = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    last_name = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    ssn = serializers.CharField(
        allow_null=True, allow_blank=True, write_only=True, required=False
    )
    social_security_number = serializers.CharField(
        read_only=True, source="user.social_security_number"
    )

    password = serializers.CharField(write_only=True)
    departments = serializers.SlugRelatedField(
        queryset=Department.objects.all(), slug_field="uid", write_only=True
    )
    department = PrivateDepartmentSlimSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    achievement = PrivateAchievementSlimWriteSerializer(
        many=True,
        allow_null=True,
        allow_empty=True,
        write_only=True,
        required=False,
    )
    achievements = PrivateAchievementSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )
    affiliation = PrivateAffiliationSlimWriteSerializer(
        many=True,
        allow_null=True,
        allow_empty=True,
        write_only=True,
        required=False,
    )
    affiliations = PrivateAffiliationSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )
    degree = PrivateDegreeSlimWriteSerializer(
        many=True,
        allow_null=True,
        allow_empty=True,
        write_only=True,
        required=False,
    )
    degrees = PrivateDegreeSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )
    expertises = PrivateExpertiseSlimWriteSerializer(
        many=True,
        allow_null=True,
        allow_empty=True,
        write_only=True,
        required=False,
    )
    expertise = PrivateExpertiseSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )
    completed_appointments = serializers.SerializerMethodField()
    due_appointments = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "uid",
            "slug",
            "image",
            "first_name",
            "last_name",
            "email",
            "phone",
            "ssn",
            "social_security_number",
            "registration_no",
            "password",
            "name",
            "consultation_fee",
            "follow_up_fee",
            "check_up_fee",
            "department",
            "departments",
            "experience",
            "expertises",
            "expertise",
            "degree",
            "degrees",
            "achievement",
            "achievements",
            "affiliation",
            "affiliations",
            "organization",
            "completed_appointments",
            "due_appointments",
        ]

        read_only_fields = ["uid", "slug", "organization", "department"]

    def get_completed_appointments(self, obj):
        total = Appointment.objects.filter(
            doctor__uid=obj.uid, status=AppointmentStatus.COMPLETED
        ).count()

        return total

    def get_due_appointments(self, obj):
        total = Appointment.objects.filter(
            doctor__uid=obj.uid, status=AppointmentStatus.SCHEDULED
        ).count()

        return total

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["expertise"] = [expertise for expertise in data["expertise"] if expertise]
        data["degrees"] = [degree for degree in data["degrees"] if degree]
        data["achievements"] = [
            achievement for achievement in data["achievements"] if achievement
        ]
        data["affiliations"] = [
            affiliation for affiliation in data["affiliations"] if affiliation
        ]
        return data

    def create(self, validated_data):
        with transaction.atomic():
            request = self.context["request"]

            image = validated_data.pop("image", None)
            first_name = validated_data.pop("first_name", None)
            last_name = validated_data.pop("last_name", None)
            email = validated_data.pop("email", None)
            phone = validated_data.pop("phone", None)
            social_security_number = validated_data.pop("ssn", None)
            registration_no = validated_data.pop("registration_no", None)
            password = validated_data.pop("password", None)
            consultation_fee = validated_data.pop("consultation_fee", 0)
            follow_up_fee = validated_data.pop("follow_up_fee", 0)
            check_up_fee = validated_data.pop("check_up_fee", 0)
            department = validated_data.pop("departments", None)
            experience = validated_data.pop("experience", 0)
            achievements = validated_data.pop("achievement", [])
            affiliations = validated_data.pop("affiliation", [])
            expertise_names = validated_data.pop("expertises", [])
            degrees = validated_data.pop("degree", [])

            if email:
                if User.objects.filter(email=email).exists():
                    raise ValidationError({"detail": "This email already exists."})

            user, _ = User.objects.get_or_create(
                phone=phone,
                defaults={
                    "username": phone,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "social_security_number": social_security_number,
                    "type": UserType.DOCTOR,
                },
            )

            user.set_password(password)
            user.save()
            organization = request.user.get_organization()

            try:
                Doctor.objects.get(user=user, organization=organization)
                raise ValidationError(
                    {"detail": "Doctor with this phone number already exists."}
                )

            except Doctor.DoesNotExist:
                doctor = Doctor.objects.create(
                    user=user,
                    organization=organization,
                    name=user.get_name(),
                    email=email,
                    phone=phone,
                    registration_no=registration_no,
                    department=department,
                    image=image,
                    experience=experience,
                    consultation_fee=consultation_fee,
                    follow_up_fee=follow_up_fee,
                    check_up_fee=check_up_fee,
                )

                expertise_connector = []
                for expertise_name in expertise_names:
                    name = expertise_name.get("name")
                    expertise, _ = Expertise.objects.get_or_create(name=name)
                    try:
                        DoctorAdditionalConnector.objects.get(
                            doctor=doctor, expertise=expertise
                        )
                    except DoctorAdditionalConnector.DoesNotExist:
                        expertise_connector.append(
                            DoctorAdditionalConnector(
                                doctor=doctor, expertise=expertise
                            )
                        )

                DoctorAdditionalConnector.objects.bulk_create(expertise_connector)

                degree_connector = []
                for degree_item in degrees:
                    name = degree_item.get("name")
                    institute = degree_item.get("institute")
                    result = degree_item.get("result")
                    passing_year = degree_item.get("passing_year")

                    degree, _ = Degree.objects.get_or_create(
                        name=name,
                        institute=institute,
                        result=result,
                        passing_year=passing_year,
                    )

                    try:
                        DoctorAdditionalConnector.objects.get(
                            doctor=doctor, degree=degree
                        )
                    except DoctorAdditionalConnector.DoesNotExist:
                        degree_connector.append(
                            DoctorAdditionalConnector(doctor=doctor, degree=degree)
                        )

                DoctorAdditionalConnector.objects.bulk_create(degree_connector)

                affiliation_connector = []
                for affiliation_item in affiliations:
                    title = affiliation_item.get("title")
                    hospital_name = affiliation_item.get("hospital_name")
                    expire_at = affiliation_item.get("expire_at")

                    affiliation, _ = Affiliation.objects.get_or_create(
                        title=title,
                        hospital_name=hospital_name,
                        expire_at=expire_at,
                        status=AffiliationStatus.ACTIVE,
                    )
                    try:
                        DoctorAdditionalConnector.objects.get(
                            doctor=doctor, affiliation=affiliation
                        )
                    except DoctorAdditionalConnector.DoesNotExist:
                        affiliation_connector.append(
                            DoctorAdditionalConnector(
                                doctor=doctor, affiliation=affiliation
                            )
                        )

                DoctorAdditionalConnector.objects.bulk_create(affiliation_connector)

                achievement_connector = []
                for achievement_item in achievements:
                    name = achievement_item.get("name")
                    source = achievement_item.get("source")
                    year = achievement_item.get("year")

                    achievement, _ = Achievement.objects.get_or_create(
                        name=name, source=source, year=year
                    )
                    try:
                        DoctorAdditionalConnector.objects.get(
                            doctor=doctor, achievement=achievement
                        )
                    except DoctorAdditionalConnector.DoesNotExist:
                        achievement_connector.append(
                            DoctorAdditionalConnector(
                                doctor=doctor, achievement=achievement
                            )
                        )

                DoctorAdditionalConnector.objects.bulk_create(achievement_connector)

            return doctor

    def update(self, instance, validated_data):
        # getting user object
        user = instance.user

        # getting user data from response
        user.first_name = validated_data.pop("first_name", instance.user.first_name)
        user.last_name = validated_data.pop("last_name", instance.user.last_name)
        # updating a user object
        user.save()

        # getting doctor data from response
        instance.image = validated_data.pop("image", instance.image)
        instance.consultation_fee = validated_data.pop(
            "consultation_fee", instance.consultation_fee
        )
        instance.follow_up_fee = validated_data.pop(
            "follow_up_fee", instance.follow_up_fee
        )
        instance.check_up_fee = validated_data.pop(
            "check_up_fee", instance.check_up_fee
        )
        instance.department = validated_data.pop("departments", instance.department)
        instance.experience = validated_data.pop("experience", instance.experience)
        instance.name = validated_data.pop("name", instance.name)

        # updating doctor object
        instance.save()

        # getting addition information of a doctor
        expertise_names = validated_data.pop("expertises", [])
        degrees = validated_data.pop("degree", [])
        affiliations = validated_data.pop("affiliation", [])
        achievements = validated_data.pop("achievement", [])

        # before update deleting all DoctorAdditional Connectors
        doctor_additional_connectors = DoctorAdditionalConnector.objects.filter(
            doctor=instance
        )
        doctor_additional_connectors.delete()

        expertise_connector = []
        for expertise_name in expertise_names:
            name = expertise_name.get("name")
            expertise, _ = Expertise.objects.get_or_create(name=name)
            try:
                DoctorAdditionalConnector.objects.get(
                    doctor=instance, expertise=expertise
                )
            except DoctorAdditionalConnector.DoesNotExist:
                expertise_connector.append(
                    DoctorAdditionalConnector(doctor=instance, expertise=expertise)
                )
        DoctorAdditionalConnector.objects.bulk_create(expertise_connector)

        degree_connector = []
        for degree_item in degrees:
            name = degree_item.get("name")
            institute = degree_item.get("institute")
            result = degree_item.get("result")
            passing_year = degree_item.get("passing_year")

            degree, _ = Degree.objects.get_or_create(
                name=name,
                institute=institute,
                result=result,
                passing_year=passing_year,
            )

            try:
                DoctorAdditionalConnector.objects.get(doctor=instance, degree=degree)
            except DoctorAdditionalConnector.DoesNotExist:
                degree_connector.append(
                    DoctorAdditionalConnector(doctor=instance, degree=degree)
                )

        DoctorAdditionalConnector.objects.bulk_create(degree_connector)

        affiliation_connector = []
        for affiliation_item in affiliations:
            title = affiliation_item.get("title")
            hospital_name = affiliation_item.get("hospital_name")
            expire_at = affiliation_item.get("expire_at")

            affiliation, _ = Affiliation.objects.get_or_create(
                title=title,
                hospital_name=hospital_name,
                expire_at=expire_at,
                status=AffiliationStatus.ACTIVE,
            )
            try:
                DoctorAdditionalConnector.objects.get(
                    doctor=instance, affiliation=affiliation
                )
            except DoctorAdditionalConnector.DoesNotExist:
                affiliation_connector.append(
                    DoctorAdditionalConnector(doctor=instance, affiliation=affiliation)
                )

        DoctorAdditionalConnector.objects.bulk_create(affiliation_connector)

        achievement_connector = []
        for achievement_item in achievements:
            name = achievement_item.get("name")
            source = achievement_item.get("source")
            year = achievement_item.get("year")

            achievement, _ = Achievement.objects.get_or_create(
                name=name, source=source, year=year
            )
            try:
                DoctorAdditionalConnector.objects.get(
                    doctor=instance, achievement=achievement
                )
            except DoctorAdditionalConnector.DoesNotExist:
                achievement_connector.append(
                    DoctorAdditionalConnector(doctor=instance, achievement=achievement)
                )

        DoctorAdditionalConnector.objects.bulk_create(achievement_connector)

        return instance


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
            "treatments",
            "recommendations",
            "diagnoses",
            "investigations",
            "examinations",
            "primary_diseases",
            "schedule_start",
            "schedule_end",
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


class PrivateDoctorAffiliationSerializer(serializers.ModelSerializer):
    organization = PrivateOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = Affiliation
        fields = [
            "uid",
            "title",
            "hospital_name",
            "expire_at",
            "status",
            "organization",
        ]


class PrivateDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ["uid", "name", "institute", "result", "passing_year", "status"]
        read_only_fields = [
            "uid",
            "name",
            "institute",
            "result",
            "passing_year",
            "status",
        ]


class PrivateDoctorAdditionalConnectorSerializer(serializers.ModelSerializer):
    degree = PrivateDegreeSerializer(read_only=True)

    class Meta:
        model = DoctorAdditionalConnector
        fields = ["degree"]


class PrivateDoctorAppointmentListSerializer(serializers.ModelSerializer):
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    doctor = PublicDoctorSlimSerializer(read_only=True)
    doctor_uid = serializers.SlugRelatedField(
        queryset=Doctor.objects.get_status_editable(),
        slug_field="uid",
        write_only=True,
        allow_null=True,
        allow_empty=True,
        required=False,
    )
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
    )

    fileitem = serializers.FileField(write_only=True, allow_null=True, required=False)
    image = serializers.ImageField(write_only=True, allow_null=True, required=False)
    seek_help_list = serializers.SerializerMethodField(read_only=True)
    allergic_medication_list = serializers.SerializerMethodField(read_only=True)
    current_medication_list = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "organization",
            "appointment_for",
            "appointment_type",
            "complication",
            "status",
            "is_visible",
            "patient",
            "doctor",
            "schedule_start",
            "schedule_end",
            "doctor_uid",
            "first_name",
            "last_name",
            "image",
            "date_of_birth",
            "phone",
            "email",
            "weight",
            "height",
            "blood_group",
            "gender",
            "fileitem",
            "seek_help_list",
            "allergic_medication_list",
            "current_medication_list",
            "file_item_list",
        ]

        read_only_fields = ["__all__"]

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance["organization"] = PublicOrganizationSlimSerializer(
            Organization.objects.get(uid=instance["organization"])
        ).data
        return instance

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
