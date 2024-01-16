import logging

from rest_framework import serializers

from accountio.models import Organization

from common.serializers import BaseModelSerializer



from versatileimagefield.serializers import VersatileImageFieldSerializer

logger = logging.getLogger(__name__)

class PrivateWeOrganizationSerializer(BaseModelSerializer):
    name = serializers.CharField(min_length=2)
    registration_no = serializers.CharField(min_length=2)

    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
        ],
        required=False,
    )
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x384", "thumbnail__1024x384"),
        ],
        required=False,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512x256", "thumbnail__512x256"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "uid",
            "serial_number",
            "name",
            "email",
            "slug",
            "registration_no",
            "address",
            "summary",
            "avatar",
            "hero",
            "image",
            "logo_wide",
            "description",
            "status",
            "policies",
            "kind",
            "phone",
            "website_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "slug", "created_at", "updated_at"]