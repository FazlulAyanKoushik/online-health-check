from rest_framework import generics

from ..serializers.we import PrivateWeOrganizationSerializer

from doctorio.rest.permissions import IsOrganizationStaff

class PrivateWeDetail(generics.RetrieveUpdateAPIView):
    serializer_class = PrivateWeOrganizationSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        current_organization = self.request.user.get_organization()
        return current_organization
