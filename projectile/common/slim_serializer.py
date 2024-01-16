from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import Organization

from appointmentio.models import (
    Medicine,
    PrescriptionMedicineConnector,
    Ingredient,
    AppointmentSeekHelpConnector,
    AppointmentMedicationConnector,
    AppointmentAllergicMedicationConnector,
    Shift,
    WeekDay,
)

from core.models import User

from doctorio.models import Doctor, Department

from mediaroomio.models import MediaImage, MediaImageConnector

from patientio.models import Patient

from .serializers import BaseModelSerializer


class PublicOrganizationSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["slug", "name"]


class PrivateOrganizationSlimSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)


class UserSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "slug",
            "first_name",
            "last_name",
            "social_security_number",
            "phone",
            "email",
            "date_of_birth",
            "gender",
            "blood_group",
            "height",
            "weight",
            "avatar",
        ]
        read_only_fields = ["__all__"]


class PrivateAppointmentPatientSlimSerializer(serializers.ModelSerializer):
    avatar = VersatileImageFieldSerializer(
        source="user.avatar",
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )
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
            "avatar",
        ]
        read_only_fields = ["__all__"]


class PrivatePatientSlimSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    date_of_birth = serializers.CharField(source="user.date_of_birth", read_only=True)
    blood_group = serializers.CharField(source="user.blood_group", read_only=True)
    height = serializers.CharField(source="user.height", read_only=True)
    weight = serializers.CharField(source="user.weight", read_only=True)
    gender = serializers.CharField(source="user.gender", read_only=True)

    class Meta:
        model = Patient
        fields = [
            "uid",
            "first_name",
            "last_name",
            "phone",
            "email",
            "date_of_birth",
            "blood_group",
            "height",
            "weight",
            "status",
            "gender",
        ]


class PrivateAffiliationSlimWriteSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=250, allow_null=True, allow_blank=True, required=False
    )
    hospital_name = serializers.CharField(
        max_length=250, allow_null=True, allow_blank=True, required=False
    )
    expire_at = serializers.DateField(allow_null=True)


class PrivateAchievementSlimWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    source = serializers.CharField(max_length=600, allow_null=True, allow_blank=True)
    year = serializers.DateField(allow_null=True)


class PrivateDegreeSlimWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300, allow_null=True, allow_blank=True)
    institute = serializers.CharField(max_length=300, allow_null=True, allow_blank=True)
    result = serializers.FloatField(default=0, allow_null=True)
    passing_year = serializers.DateField(allow_null=True)


class PrivateExpertiseSlimWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)


class PrivateAffiliationSlimReadSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="affiliation.uid")
    title = serializers.CharField(read_only=True, source="affiliation.title")
    hospital_name = serializers.CharField(
        read_only=True, source="affiliation.hospital_name"
    )
    expire_at = serializers.DateField(read_only=True, source="affiliation.expire_at")


class PrivateAchievementSlimReadSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="achievement.uid")
    name = serializers.CharField(read_only=True, source="achievement.name")
    source = serializers.CharField(read_only=True, source="achievement.source")
    year = serializers.DateField(read_only=True, source="achievement.year")


class PrivateDegreeSlimReadSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="degree.uid")
    name = serializers.CharField(read_only=True, source="degree.name")
    institute = serializers.CharField(read_only=True, source="degree.institute")
    result = serializers.FloatField(read_only=True, source="degree.result")
    passing_year = serializers.DateField(read_only=True, source="degree.passing_year")


class PrivateExpertiseSlimReadSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="expertise.uid")
    name = serializers.CharField(read_only=True, source="expertise.name")


class PublicDoctorSlimSerializer(BaseModelSerializer):
    degrees = PrivateDegreeSlimReadSerializer(
        source="doctoradditionalconnector_set", many=True
    )
    department_name = serializers.CharField(
        source="department.name", allow_null=True, allow_blank=True
    )

    class Meta:
        model = Doctor
        fields = [
            "slug",
            "serial_number",
            "name",
            "email",
            "phone",
            "degrees",
            "image",
            "department_name",
        ]
        read_only_fields = ("__all__",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["degrees"] = [degree for degree in data["degrees"] if degree]

        return data


class GlobalImageSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaImage
        fields = (
            "slug",
            "image",
        )
        read_only_fields = ("__all__",)


class GlobalMediaImageConnectorSlimSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        source="image.image",
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )

    class Meta:
        model = MediaImageConnector
        fields = ("image",)
        read_only_fields = ("__all__",)


class MedicineDoseSlimSerializer(serializers.Serializer):
    medicine_uid = serializers.SlugRelatedField(
        queryset=Medicine.objects.all(), slug_field="uid", write_only=True
    )
    interval = serializers.CharField(max_length=255)
    duration = serializers.CharField(max_length=255)
    indication = serializers.CharField(max_length=255)


class RecommendationSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="recommendation.name", max_length=255, read_only=True
    )


class DiagnosisSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="diagnosis.name", max_length=255, read_only=True
    )


class InvestigationSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="investigation.name", max_length=255, read_only=True
    )


class ExaminationSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="examination.name", max_length=255, read_only=True
    )


class PrimaryDiseaseSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="primary_disease.name", max_length=255, read_only=True
    )


class MedicineSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["uid", "name", "strength"]


class PrescriptionMedicineConnectorTreatmentSlimSerializer(serializers.ModelSerializer):
    medicine = MedicineSlimSerializer(read_only=True)
    duration = serializers.CharField(source="dosage")
    indication = serializers.CharField(source="frequency")

    class Meta:
        model = PrescriptionMedicineConnector
        fields = ["medicine", "interval", "indication", "duration"]


class PrivateDoctorSlimSerializer(serializers.ModelSerializer):
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
    display_email = serializers.EmailField(source="email", required=False)
    display_phone = PhoneNumberField(required=False, source="phone")

    expertise = PrivateExpertiseSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )

    class Meta:
        model = Doctor
        fields = [
            "uid",
            "name",
            "display_email",
            "display_phone",
            "department",
            "image",
            "slug",
            "expertise",
        ]


class PrivateOrganizationSlimSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)


class PublicDegreeSlimSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True, source="degree.name")


class IngredientSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["uid", "slug", "name"]


class PrivateDepartmentSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["uid", "name"]


class PrivateAllergicMedicineSlimSerializer(serializers.Serializer):
    medicine = serializers.CharField(source="medicine.name")
    other = serializers.CharField()


class PrivateSeekHelpSlimSerializer(serializers.Serializer):
    name = serializers.CharField()


class PrivateAppointmentMedicationConnectorSlimSerializer(serializers.Serializer):
    medicine = serializers.CharField()
    usage = serializers.CharField(allow_blank=True, allow_null=True)


class PrivateSeekHelpSlimSerializer(serializers.ModelSerializer):
    seek_help_for = serializers.SerializerMethodField(read_only=True)

    def get_seek_help_for(self, obj):
        if obj.seek_help:
            return obj.seek_help.name
        else:
            return obj.seek_help_for

    class Meta:
        model = AppointmentSeekHelpConnector
        fields = ["seek_help_for"]
        read_only_fields = ("__all__",)


class PrivateAllergicMedicationSlimSerializer(serializers.ModelSerializer):
    medicine_name = serializers.SerializerMethodField(read_only=True)

    def get_medicine_name(self, obj):
        if obj.medicine:
            return obj.medicine.name
        else:
            return obj.other_medicine

    class Meta:
        model = AppointmentAllergicMedicationConnector
        fields = ["medicine_name"]
        read_only_fields = ("__all__",)


class PrivateCurrentMedicationSlimSerializer(serializers.ModelSerializer):
    medicine_name = serializers.SerializerMethodField(read_only=True)

    def get_medicine_name(self, obj):
        if obj.medicine:
            return obj.medicine.name
        else:
            return obj.other_medicine

    class Meta:
        model = AppointmentMedicationConnector
        fields = ["medicine_name", "usage"]
        read_only_fields = ("__all__",)


class PrivateMediaImageConnectorSlimSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="image.uid")
    image = serializers.ImageField(
        source="image.image", allow_null=True, read_only=True, required=False
    )
    fileitem = serializers.FileField(
        source="image.fileitem", allow_null=True, read_only=True, required=False
    )
    kind = serializers.CharField(source="image.kind", read_only=True, required=False)
    caption = serializers.CharField(
        source="image.caption", read_only=True, required=False
    )

    class Meta:
        model = MediaImageConnector
        fields = ["uid", "kind", "caption", "image", "fileitem"]


class PrivateShiftWriteSlimSerializer(serializers.Serializer):
    shift_label = serializers.CharField(
        max_length=50, allow_blank=True, allow_null=True, required=False
    )
    start_time = serializers.TimeField(allow_null=True, required=False)
    end_time = serializers.TimeField(allow_null=True, required=False)


class PrivateWeekDayWriteSlimSerializer(serializers.Serializer):
    day = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    off_day = serializers.BooleanField(default=False)
    shift = PrivateShiftWriteSlimSerializer(many=True, allow_null=True, required=False)
