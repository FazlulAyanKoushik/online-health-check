from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import Organization

from doctorio.models import Doctor

from common import slim_serializer


class PublicOrganizationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["uid", "slug", "name"]
        read_only_fields = ["__all__"]


class PublicOrganizationDoctorsSerializers(serializers.ModelSerializer):
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
    expertise = slim_serializer.PrivateExpertiseSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )

    class Meta:
        model = Doctor
        fields = [
            "slug",
            "name",
            "email",
            "phone",
            "registration_no",
            "department",
            "image",
            "expertise",
            "experience",
            "consultation_fee",
            "follow_up_fee",
            "check_up_fee",
            "status",
        ]

        read_only_fields = ("__all__",)
